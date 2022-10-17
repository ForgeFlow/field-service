# Copyright (C) 2022 ForgeFlow S.L
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Field Service - Analysis",
    "summary": "Adds economic analysis to the Field Service Order",
    "version": "14.0.1.0.0",
    "category": "Field Service",
    "author": "Forgeflow, ",
    "website": "https://github.com/OCA/field-service",
    "depends": ["fieldservice_sale_stock",
                "fieldservice_stock_request"],
    "data": [
        # "security/ir.model.access.csv",
        "views/fsm_order.xml",
    ],
    "license": "AGPL-3",
    "development_status": "Beta",
}
