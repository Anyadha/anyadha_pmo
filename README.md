# Anyadha PMO v2.0.0

Enterprise PMO application for Frappe Framework 16 / ERPNext 16.

## Architecture
Anyadha PMO is a governance and management layer over native ERPNext transactions. It does not duplicate ERPNext accounting, procurement, HR, inventory, asset or tax transaction engines.

## Functional domains
- PMO Masters
- Governance & Board
- Delegation & Approvals
- Strategy & Portfolio
- Proposal & DPR
- Programme & Project Management
- Monitoring & Evaluation
- Grants & Donor Management
- CSR Management
- Risk & Internal Controls
- Compliance & Regulatory
- Audit & Assurance
- SOP & Document Control
- KPI, MIS & Performance

## Frappe target
Frappe >=16,<17
Python >=3.10,<3.15

## Installation
Install this app on an ERPNext v16 site. Do not install as a replacement for ERPNext.

## Validation
Run:
    python validate_app.py

The validator checks package structure, JSON syntax, DocType/module consistency, controller references, and duplicate DocType names.

## Important design principle
Native ERPNext remains the transaction system of record for accounting, purchasing, stock, assets, HR/payroll and related transactions. Anyadha PMO provides governance, planning, monitoring, compliance, assurance and executive reporting around those transactions.
