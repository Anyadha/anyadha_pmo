/* Required quotation-document step for the standard ERPNext supplier RFQ page.
 *
 * Website/portal pages only load frappe-web.bundle.js + bootstrap-4-web.bundle.js,
 * not the desk form-control library, so frappe.ui.Dialog cannot be used here
 * (frappe.ui.form.make_control is undefined on this bundle). The attach dialog
 * is built as a plain Bootstrap 4 modal instead, the same pattern Frappe's own
 * website discussion modal uses (frappe/templates/discussions/discussions.js).
 */
(function () {
	"use strict";

	function isRfqPage() {
		return window.doc && window.doc.doctype === "Request for Quotation";
	}

	function makePayload() {
		return {
			name: window.doc.name,
			terms: $(".terms-feedback").val() || "",
			items: (window.doc.items || []).map(function (item) {
				var selector = '[data-idx="' + item.idx + '"]';
				return {
					name: item.name,
					// Read the fields now as well as window.doc. This includes a value
					// typed immediately before the button is clicked (before blur/change).
					qty: $(".rfq-qty" + selector).val(),
					rate: $(".rfq-rate" + selector).val()
				};
			})
		};
	}

	function refreshSubmitButtonState($modal, $submitBtn) {
		var input = $modal.find(".anyadha-quotation-file")[0];
		var has_file = !!(input && input.files && input.files.length);
		var $label = $modal.find(".anyadha-quotation-file-label");
		var $hint = $modal.find(".anyadha-quotation-hint");

		$submitBtn.prop("disabled", !has_file);
		$submitBtn.attr("title", has_file ? "" : __("Please attach your quotation document (PDF, Excel, Word, or image) before creating the quotation."));

		if (has_file) {
			$label.text(input.files[0].name).removeClass("text-muted").addClass("text-dark");
			$hint.removeClass("alert-warning").addClass("alert-success")
				.html('<i class="fa fa-check-circle mr-1"></i>' + __("Ready to submit: {0}", [$("<div>").text(input.files[0].name).html()]));
		} else {
			$label.text(__("Choose file...")).removeClass("text-dark").addClass("text-muted");
			$hint.removeClass("alert-success").addClass("alert-warning")
				.html('<i class="fa fa-exclamation-triangle mr-1"></i>' + __("Please attach your quotation document (PDF, Excel, Word, or image) before creating the quotation."));
		}
	}

	function submitWithAttachment($modal, $submitBtn) {
		var input = $modal.find(".anyadha-quotation-file")[0];
		if (!input || !input.files || !input.files.length) {
			frappe.msgprint(__("Please attach your quotation document (PDF, Excel, Word, or image) before creating the quotation."));
			return;
		}

		var formData = new FormData();
		formData.append("file", input.files[0]);
		formData.append("method", "anyadha_pmo.api.supplier_rfq_quotation.create_supplier_quotation_with_attachment");
		formData.append("doc", JSON.stringify(makePayload()));

		$submitBtn.prop("disabled", true);
		frappe.freeze(__("Creating Supplier Quotation..."));
		$.ajax({
			url: "/api/method/upload_file",
			type: "POST",
			data: formData,
			processData: false,
			contentType: false,
			headers: { "X-Frappe-CSRF-Token": frappe.csrf_token },
			success: function (response) {
				var quotationName = response.message;
				if (quotationName) {
					$modal.modal("hide");
					frappe.show_alert({
						message: __("Supplier Quotation {0} created", [quotationName]),
						indicator: "green"
					});
					window.location.href = "/rfq";
				}
			},
			error: function (xhr) {
				var message = __("Unable to create the quotation.");
				var serverMessages = xhr.responseJSON && xhr.responseJSON._server_messages;
				if (serverMessages) {
					try {
						var messages = JSON.parse(serverMessages);
						message = JSON.parse(messages[0]).message || message;
					} catch (ignore) {}
				}
				frappe.msgprint(message);
				$submitBtn.prop("disabled", false);
			},
			complete: function () {
				frappe.unfreeze();
			}
		});
	}

	function showAttachmentDialog() {
		// Remove any previous instance so repeated opens don't stack modal-backdrops.
		$(".anyadha-quotation-modal").remove();

		var $modal = $(
			'<div class="modal fade anyadha-quotation-modal" tabindex="-1" role="dialog" aria-labelledby="anyadhaQuotationModalTitle" aria-hidden="true">' +
				'<div class="modal-dialog modal-dialog-centered" role="document">' +
					'<div class="modal-content">' +
						'<div class="modal-header bg-light">' +
							'<h5 class="modal-title" id="anyadhaQuotationModalTitle">' +
								'<i class="fa fa-paperclip text-muted mr-2"></i>' + __("Attach Your Quotation") +
							'</h5>' +
							'<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
						'</div>' +
						'<div class="modal-body">' +
							'<p>' + __("Upload your quotation document (PDF, Excel, Word, or image) before creating the draft quotation.") + '</p>' +
							'<div class="custom-file mb-3">' +
								'<input type="file" class="custom-file-input anyadha-quotation-file" accept=".pdf,.xls,.xlsx,.doc,.docx,.jpg,.jpeg,.png" required>' +
								'<label class="custom-file-label anyadha-quotation-file-label text-muted" for="">' + __("Choose file...") + '</label>' +
							'</div>' +
							'<small class="form-text text-muted mb-3 d-block">' + __("Accepted formats: PDF, XLS, XLSX, DOC, DOCX, JPG, PNG") + '</small>' +
							'<div class="alert alert-warning anyadha-quotation-hint mb-0 py-2 px-3 small">' +
								'<i class="fa fa-exclamation-triangle mr-1"></i>' +
								__("Please attach your quotation document (PDF, Excel, Word, or image) before creating the quotation.") +
							'</div>' +
						'</div>' +
						'<div class="modal-footer">' +
							'<button type="button" class="btn btn-secondary" data-dismiss="modal">' + __("Cancel") + '</button>' +
							'<button type="button" class="btn btn-primary anyadha-quotation-submit" disabled>' +
								'<i class="fa fa-check mr-1"></i>' + __("Make Quotation") +
							'</button>' +
						'</div>' +
					'</div>' +
				'</div>' +
			'</div>'
		).appendTo("body");

		var $submitBtn = $modal.find(".anyadha-quotation-submit");

		$modal.on("change", ".anyadha-quotation-file", function () {
			refreshSubmitButtonState($modal, $submitBtn);
		});
		$submitBtn.on("click", function () {
			submitWithAttachment($modal, $submitBtn);
		});
		$modal.on("hidden.bs.modal", function () {
			$modal.remove();
		});

		$modal.modal("show");
	}

	function replaceStandardHandler() {
		if (!isRfqPage()) return;

		var buttons = $("button.btn.btn-primary.btn-sm").filter(function () {
			return $(this).text().trim() === __("Make Quotation");
		});
		buttons.off("click").on("click.anyadhaSupplierQuotation", function (event) {
			event.preventDefault();
			showAttachmentDialog();
		});
	}

	// ERPNext attaches its direct click handler during document-ready. Queue this
	// after it, then replace only the RFQ's Make Quotation handler.
	$(document).ready(function () {
		window.setTimeout(replaceStandardHandler, 0);
	});
})();
