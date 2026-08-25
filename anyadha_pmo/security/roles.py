"""Anyadha PMO role definitions.

Roles are provisioned by install.py and remain normal Frappe Role records.
This file is only the application-level source of truth for PMO role names.
"""

PMO_ROLES = [
    ("PMO Administrator", 1),
    ("PMO Head", 1),
    ("Programme Manager", 1),
    ("Project Manager", 1),
    ("PMO Officer", 1),
    ("M&E Manager", 1),
    ("M&E Officer", 1),
    ("Grants Manager", 1),
    ("CSR Manager", 1),
    ("Compliance Officer", 1),
    ("Internal Auditor", 1),
    ("Executive / Management", 1),
    ("Board Member", 1),
]

PMO_ROLE_NAMES = {name for name, _ in PMO_ROLES}
