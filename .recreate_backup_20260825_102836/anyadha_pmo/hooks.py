app_name = "anyadha_pmo"
app_title = "Anyadha PMO"
app_publisher = "Anyadha"
app_description = "Enterprise PMO - Governance, Programme, Project, M&E, Grants, CSR, Compliance, Audit and MIS"
app_email = "info@anyadha.com"
app_license = "MIT"

# Keep hooks deliberately minimal in v2.0. Business rules belong in DocType controllers.

after_install = "anyadha_pmo.install.after_install"
after_migrate = "anyadha_pmo.install.after_migrate"
