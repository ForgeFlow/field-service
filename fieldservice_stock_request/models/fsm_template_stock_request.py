# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FSMTemplate(models.Model):
    _name = "fsm.template.stock.request"

    template_id = fields.Many2one(comodel_name='fsm.template')
    product_id = fields.Many2one(comodel_name='product.product',
                                 domain=[("type", "in", ("product", "consu"))])
    product_uom_id = fields.Many2one(comodel_name="uom.uom", string="UoM")
    product_uom_qty = fields.Float()
    direction = fields.Selection(
        [("outbound", "Outbound"), ("inbound", "Inbound")],
        string="Direction",
    )
