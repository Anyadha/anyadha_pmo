frappe.ui.form.on("PMO Approval Request", {
    refresh(frm) {
        if (frm.doc.workflow_state) {
            frm.dashboard.set_headline_alert(__("Workflow: {0}", [frm.doc.workflow_state]));
        }
    },
});
