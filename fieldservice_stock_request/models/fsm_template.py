# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FSMTemplate(models.Model):
    _inherit = "fsm.template"

    stock_request_ids = fields.One2many(
        comodel_name='fsm.template.stock.request',
        inverse_name='template_id'
    )
