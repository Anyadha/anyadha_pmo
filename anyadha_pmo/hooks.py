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

# Native Frappe v16 Apps Page / Desk app registration.
add_to_apps_screen = [{
    "name": "anyadha_pmo",
    "title": "Anyadha PMO",
    "route": "/desk/executive-pmo",
    "sequence_id": 50,
}]
