/* Required quotation-document step for the standard ERPNext supplier RFQ page. */
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

	function submitWithAttachment(dialog, button) {
		var input = dialog.$wrapper.find(".anyadha-quotation-file")[0];
		if (!input || !input.files || !input.files.length) {
			frappe.msgprint(__("Please attach your quotation document."));
			return;
		}

		var formData = new FormData();
		formData.append("file", input.files[0]);
		formData.append("method", "anyadha_pmo.api.supplier_rfq_quotation.create_supplier_quotation_with_attachment");
		formData.append("doc", JSON.stringify(makePayload()));

		button.prop("disabled", true);
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
					dialog.hide();
					window.location.href = "/supplier-quotations/" + encodeURIComponent(quotationName);
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
				button.prop("disabled", false);
			},
			complete: function () {
				frappe.unfreeze();
			}
		});
	}

	function showAttachmentDialog() {
		var dialog = new frappe.ui.Dialog({
			title: __("Attach Your Quotation"),
			fields: [{
				fieldtype: "HTML",
				fieldname: "quotation_file_html",
				options: '<p class="text-muted">' + __("Upload the quotation document before creating the draft quotation.") + '</p>' +
					'<input class="anyadha-quotation-file" type="file" accept=".pdf,.xls,.xlsx,.doc,.docx" required>'
			}],
			primary_action_label: __("Make Quotation"),
			primary_action: function () {
				submitWithAttachment(dialog, dialog.get_primary_btn());
			}
		});
		dialog.show();
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
