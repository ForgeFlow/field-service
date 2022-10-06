# Copyright (C) 2022 ForgeFlow, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class FSMOrder(models.Model):
    _inherit = "fsm.order"

    sale_invoice_plan_ids = fields.One2many(
        "sale.invoice.plan",
        string="Invoice Plan",
        compute="_compute_sale_invoice_plan_ids"
    )
    sale_invoice_plan_count = fields.Integer(
        string="# Invoice Plan Lines",
        compute="_compute_sale_invoice_plan_ids"
    )

    def _compute_sale_invoice_plan_ids(self):
        for rec in self:
            plan_lines = rec.mapped("sale_id.invoice_plan_ids")
            rec.sale_invoice_plan_ids = plan_lines.filtered(
                lambda p: p.invoice_type != 'advance')
            rec.sale_invoice_plan_count = len(plan_lines)

    def action_view_sales_invoice_plan(self):
        self.ensure_one()
        action = self.env.ref(
            "fieldservice_sale_invoice_plan.action_sale_invoice_plan_fsm_order")
        result = action.read()[0]
        result["domain"] = [("id", "in", self.sale_invoice_plan_ids.ids)]
        return result
