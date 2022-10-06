# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Field Service Sales Invoice Plan",
    "summary": "Allows to indicate from the FSM Order what invoice plan lines "
               "are ready to invoice",
    "version": "14.0.1.0.1",
    "author": "ForgeFlow,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/field-service",
    "category": "Sales",
    "depends": ["fieldservice_sale", "sale_invoice_plan_manual_release"],
    "data": [
        "views/sale_view.xml",
        "views/fsm_order_view.xml"
    ],
    "installable": True,
    "development_status": "Alpha",
    "maintainers": ["jordibforgeflow"],
}
