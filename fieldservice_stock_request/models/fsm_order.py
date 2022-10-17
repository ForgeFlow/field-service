# Copyright (C) 2021 - TODAY, Brian McMaster
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

REQUEST_STATES = [
    ("draft", "Draft"),
    ("submitted", "Submitted"),
    ("open", "In progress"),
    ("done", "Done"),
    ("cancel", "Cancelled"),
]


class FSMOrder(models.Model):
    _inherit = "fsm.order"

    stock_request_ids = fields.One2many(
        "stock.request", "fsm_order_id", string="Order Lines"
    )
    request_stage = fields.Selection(
        REQUEST_STATES,
        string="Request State",
        default="draft",
        readonly=True,
    )

    def action_request_submit(self):
        for rec in self:
            if not rec.stock_request_ids:
                raise UserError(_("Please create a stock request."))
            for line in rec.stock_request_ids.filtered(lambda l: l.state == "draft"):
                if ("submitted", "Submitted") in line._get_request_states():
                    if line.order_id:
                        line.order_id.action_submit()
                    else:
                        line.action_submit()
                else:
                    if line.order_id:
                        line.order_id.action_confirm()
                    else:
                        line.action_confirm()
            rec.request_stage = "submitted"

    def action_request_cancel(self):
        for rec in self:
            if not rec.stock_request_ids:
                raise UserError(_("Please create a stock request."))
            for line in rec.stock_request_ids.filtered(
                lambda l: l.state in ("draft", "open")
            ):
                if line.order_id:
                    line.order_id.action_cancel()
                else:
                    line.action_cancel()
            rec.request_stage = "cancel"

    def action_request_draft(self):
        for rec in self:
            if not rec.stock_request_ids:
                raise UserError(_("Please create a stock request."))
            for line in rec.stock_request_ids.filtered(lambda l: l.state == "cancel"):
                if line.order_id:
                    line.order_id.action_draft()
                else:
                    line.action_draft()
            rec.request_stage = "draft"

    def _prepare_stock_request_data(self, srt):
        self.ensure_one()
        uom = srt.product_uom_id or srt.product_id.uom_id

        data = {
            "product_id": srt.product_id.id,
            "product_uom_id": uom.id,
            "product_uom_qty": srt.product_uom_qty,
            "direction": srt.direction,
            "expected_date": self.scheduled_date_start,
            "picking_policy": 'direct'
        }
        if srt.direction == "outbound":
            # Inventory location of the FSM location of the order
            location = self.location_id.inventory_location_id
        else:
            location = self.warehouse_id.lot_stock_id.id
        if location:
            data['location_id'] = location.id
        return data

    @api.onchange("template_id")
    def _update_stock_requests_from_template(self):
        for rec in self:
            # Cancel existing stock requests
            for sr in rec.stock_request_ids:
                if sr.state == 'draft':
                    sr.action_cancel()
            if rec.template_id:
                stock_request_list = []
                for srt in rec.template_id.stock_request_ids:
                    sr_data = rec._prepare_stock_request_data(srt)
                    stock_request_list.append(
                        (
                            0,
                            0,
                            sr_data,
                        )
                    )
                rec.stock_request_ids = stock_request_list

    @api.model
    def create(self, vals):
        """Update Activities for FSM orders that are generate from SO"""
        order = super(FSMOrder, self).create(vals)
        order._update_stock_requests_from_template()
        return order
