# Anyadha PMO v2.0 Architecture

## Source basis
The design is based on Draft SOP Manual 1.0 and the agreed PMO architecture. The SOP requires governance, authority, project/programme management, grant/CSR/donor controls, compliance, risk/internal controls, audit, document control, KPI/MIS and integrated ERP governance.

## Native ERPNext domains retained
Company, User, Employee, Customer, Supplier, Project, Task, Purchase transactions, Sales transactions, Accounting, Cost Center, Budget, Asset, Stock, HR/Payroll and statutory transaction/reporting engines remain native ERPNext wherever applicable.

## PMO custom domains
Governance, approvals/DoA, strategy/portfolio, proposal/DPR, programme/project governance, M&E, grants/donor/CSR governance, risk/control, compliance, audit, SOP/document control, KPI/MIS.

## Design rules
- No duplicate accounting engine.
- No duplicate procurement transaction engine.
- No duplicate employee/payroll engine.
- Use Link fields to native ERPNext masters where applicable.
- Keep approval logic server-side.
- Use workflows for controlled approval states.
- Use child tables for repeated structured data.
- Preserve auditability and evidence links.
