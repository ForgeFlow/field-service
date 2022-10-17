from odoo import api, fields, models


class FSMOrder(models.Model):
    _inherit = "fsm.order"

    currency_id = fields.Many2one("res.currency", string="Currency", computed="_compute_currency")
    planned_revenue = fields.Monetary(string="Planned Revenue", compute="_compute_planned_revenue", currency_field="currency_id")
    planned_cost = fields.Monetary(string="Planned Cost", compute="_compute_planned_cost", currency_field="currency_id")
    planned_profit = fields.Monetary(string="Planned Profit", compute="_compute_profit", currency_field="currency_id")
    planned_margin = fields.Float(string="Planned Margin (%)",  compute="_compute_profit")
    actual_revenue = fields.Monetary(string="Actual Revenue", compute="_compute_actual_revenue", currency_field="currency_id")
    actual_cost = fields.Monetary(string="Actual Cost", compute="_compute_actual_cost", currency_field="currency_id")
    actual_profit = fields.Monetary(string="Actual Profit", compute="_compute_profit", currency_field="currency_id")
    actual_margin = fields.Float(string="Actual Margin (%)", compute="_compute_profit")

    def _compute_currency(self):
        for rec in self:
            rec.currency_id = rec.company_id.currency_id

    def _compute_planned_revenue(self):
        for rec in self:
            rec.planned_revenue = 0.0
            if rec.sale_line_id:
                rec.planned_revenue += rec.sale_line_id.price_subtotal
            elif rec.sale_id:
                rec.planned_revenue += rec.sale_id.amount_untaxed

    def _compute_planned_cost(self):
        for rec in self:
            rec.planned_cost = 0.0
            if rec.stock_request_ids:
                for line in rec.stock_request_ids:
                    rec.planned_cost += line.product_id.standard_price * line.product_uom_qty

    def _compute_actual_revenue(self):
        for rec in self:
            rec.actual_revenue = 0.0
            if rec.invoice_lines:
                posted_invoice_lines = rec.invoice_lines.filtered(lambda l: l.parent_state == 'posted')
                rec.actual_revenue += sum(posted_invoice_lines.mapped('price_subtotal'))

    def _compute_actual_cost(self):
        for rec in self:
            rec.actual_cost = 0.0
            if rec.move_ids:
                for move in rec.move_ids:
                    rec.actual_cost += move.product_id.standard_price * move.quantity_done

    def _compute_profit(self):
        for rec in self:
            rec.planned_profit = rec.planned_revenue - rec.planned_cost
            rec.actual_profit = rec.actual_revenue - rec.actual_cost
            rec.planned_margin = 0.0
            rec.actual_margin = 0.0
            if rec.planned_revenue:
                rec.planned_margin = round(rec.planned_profit/rec.planned_revenue, 2) * 100
            if rec.actual_revenue:
                rec.actual_margin = round(rec.actual_profit/rec.actual_revenue, 2) * 100

