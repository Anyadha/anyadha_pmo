app_name = "anyadha_pmo"
app_title = "Anyadha PMO"
app_publisher = "Anyadha"
app_description = (
    "Anyadha Enterprise PMO - Governance, Strategy, Programme, Project, "
    "M&E, Grants, CSR, Risk, Compliance, Audit and MIS"
)
app_email = "info@anyadha.com"
app_license = "MIT"
app_version = "2.1.0"

required_apps = ["erpnext"]

after_install = "anyadha_pmo.install.after_install"
after_migrate = "anyadha_pmo.install.after_migrate"

# Frappe v16 application registration.

app_logo_url = "/assets/anyadha_pmo/images/anyadha-pmo-logo.svg"

app_home = "/desk/executive-pmo"

add_to_apps_screen = [
    {
        "name": app_name,
        "logo": app_logo_url,
        "title": app_title,
        "route": app_home,
        "has_permission": "anyadha_pmo.api.app.check_app_permission",
        "sequence_id": 10,
    }
]


override_doctype_class = {
    "PMO Project": "anyadha_pmo.project_management.doctype.pmo_project.pmo_project.PmoProject",
}
