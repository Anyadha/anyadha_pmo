"""Secure supplier-portal RFQ quotation creation with a required attachment."""

from __future__ import annotations

import math
import os
from contextlib import contextmanager

import frappe
from frappe import _
from frappe.utils import flt

from erpnext.buying.doctype.request_for_quotation.request_for_quotation import (
	make_supplier_quotation_from_rfq,
	validate_existing_supplier_quotation,
)


ALLOWED_EXTENSIONS = {".pdf", ".xls", ".xlsx", ".doc", ".docx", ".jpg", ".jpeg", ".png"}


@frappe.whitelist(methods=["POST"])
def create_supplier_quotation_with_attachment(doc: str | dict | None = None):
	"""Create one draft Supplier Quotation from a supplier's RFQ portal response.

	This method is invoked by ``/api/method/upload_file``.  The upload handler
	places the uploaded bytes in ``frappe.local.uploaded_file`` before calling us.
	Only rate, quantity and terms supplied by the portal are used; every other
	quotation value is mapped from the submitted RFQ on the server.
	"""
	if frappe.session.user == "Guest":
		frappe.throw(_("Please log in to create a quotation."), frappe.PermissionError)

	# ``upload_file`` invokes its callback with no positional arguments; values
	# posted alongside the file are available through form_dict.
	payload = frappe.parse_json(doc or frappe.form_dict.get("doc"))
	rfq_name = payload.get("name")
	if not rfq_name:
		frappe.throw(_("Request for Quotation is required."))

	rfq = frappe.get_doc("Request for Quotation", rfq_name)
	if rfq.docstatus != 1:
		frappe.throw(_("Request for Quotation must be submitted before a quotation can be created."))

	supplier = _get_authorized_supplier(rfq)
	_validate_upload()
	portal_items = _validate_and_normalize_items(rfq, payload.get("items"))

	# Locks the RFQ before the duplicate check, matching ERPNext's portal flow.
	validate_existing_supplier_quotation(supplier, [{"parent": rfq.name}])

	# Start from ERPNext's standard RFQ-to-Supplier-Quotation mapping.  This
	# preserves all standard fields and references; only editable portal values
	# are overlaid after the server has verified their RFQ item identities.
	# ``make_supplier_quotation_from_rfq`` runs its own doctype-level
	# permission check (via get_mapped_doc) before returning, and the portal
	# user intentionally has no Desk create permission for Supplier Quotation.
	# Authorization for *this* supplier/RFQ pair was already verified above,
	# so elevate only for this mapping call.
	with _elevated_permission_user():
		sq = make_supplier_quotation_from_rfq(rfq.name, for_supplier=supplier)

	sq.terms = payload.get("terms") or ""

	for row in sq.items:
		portal_row = portal_items[row.request_for_quotation_item]
		row.qty = portal_row["qty"]
		row.rate = portal_row["rate"]

	# This is a controlled server-side save for a verified portal supplier.  The
	# user intentionally has no Desk permission to create Supplier Quotations.
	sq.flags.ignore_permissions = True
	sq.save()

	attachment_content = frappe.local.uploaded_file
	if os.path.splitext(frappe.local.uploaded_filename)[1].lower() == ".pdf":
		attachment_content = _compress_pdf_if_possible(attachment_content)

	frappe.get_doc(
		{
			"doctype": "File",
			"file_name": os.path.basename(frappe.local.uploaded_filename),
			"attached_to_doctype": "Supplier Quotation",
			"attached_to_name": sq.name,
			"is_private": 1,
			"content": attachment_content,
		}
	).save(ignore_permissions=True)

	frappe.msgprint(_("Supplier Quotation {0} Created").format(sq.name))
	return sq.name


@contextmanager
def _elevated_permission_user():
	"""Run permission checks as Administrator without disturbing the request's session.

	``frappe.set_user()`` is unsafe for a temporary elevate/restore here: besides
	``session.user`` it also overwrites ``session.sid`` with the literal username
	and wipes ``session.data``. Restoring with ``frappe.set_user(portal_user)``
	afterward would then leave ``session.sid`` set to the portal user's *name*
	instead of their real (random) session id, corrupting the session record
	written back at the end of the request and effectively logging them out.
	Only the fields permission checks actually consult are swapped here.
	"""
	original_user = frappe.local.session.user
	original_user_perms = frappe.local.user_perms
	frappe.local.session.user = "Administrator"
	frappe.local.user_perms = None
	try:
		yield
	finally:
		frappe.local.session.user = original_user
		frappe.local.user_perms = original_user_perms


def _get_authorized_supplier(rfq):
	"""Return the sole RFQ supplier associated with the current portal user."""
	portal_suppliers = set(
		frappe.get_all(
			"Portal User",
			filters={"parenttype": "Supplier", "user": frappe.session.user},
			pluck="parent",
		)
	)
	authorized_suppliers = [row.supplier for row in rfq.suppliers if row.supplier in portal_suppliers]

	if len(authorized_suppliers) != 1:
		frappe.throw(_("You are not permitted to create a quotation for this Request for Quotation."), frappe.PermissionError)

	return authorized_suppliers[0]


def _validate_and_normalize_items(rfq, supplied_items):
	if not isinstance(supplied_items, list) or not supplied_items:
		frappe.throw(_("Quotation items are required."))

	rfq_item_names = {row.name for row in rfq.items}
	portal_items = {}
	for item in supplied_items:
		item = frappe._dict(item)
		item_name = item.get("name")
		if item_name not in rfq_item_names or item_name in portal_items:
			frappe.throw(_("Quotation contains an invalid Request for Quotation item."), frappe.PermissionError)

		qty = flt(item.get("qty"))
		rate = flt(item.get("rate"))
		if not math.isfinite(qty) or not math.isfinite(rate) or qty < 0 or rate < 0:
			frappe.throw(_("Quantity and rate must be valid non-negative numbers."))

		portal_items[item_name] = {"qty": qty, "rate": rate}

	if set(portal_items) != rfq_item_names:
		frappe.throw(_("Quotation must contain every item from the Request for Quotation."))

	return portal_items


def _validate_upload():
	filename = frappe.local.uploaded_filename or ""
	content = frappe.local.uploaded_file
	if not filename or not content:
		frappe.throw(_("Please attach your quotation document."))

	if os.path.splitext(filename)[1].lower() not in ALLOWED_EXTENSIONS:
		frappe.throw(_("Attach a PDF, Excel, Word, or image (JPG/PNG) quotation document."))


def _compress_pdf_if_possible(content: bytes) -> bytes:
	"""Best-effort content-stream compression for PDF uploads.

	Falls back to the original bytes for encrypted, malformed, or
	non-shrinking PDFs so an upload is never blocked by compression.
	"""
	from io import BytesIO

	try:
		from pypdf import PdfReader, PdfWriter

		reader = PdfReader(BytesIO(content))
		if reader.is_encrypted:
			return content

		writer = PdfWriter()
		for page in reader.pages:
			writer.add_page(page)
		for page in writer.pages:
			page.compress_content_streams()

		buffer = BytesIO()
		writer.write(buffer)
		compressed = buffer.getvalue()
	except Exception:
		frappe.log_error(title="Supplier quotation PDF compression failed")
		return content

	return compressed if len(compressed) < len(content) else content
