frappe.ui.form.on("PMO Settings", {
    refresh(frm) {
        frm.set_intro(__("PMO governance controls are applied server-side. Changes to approval, scope, evidence and security settings should be reviewed before saving."));
    },
});
