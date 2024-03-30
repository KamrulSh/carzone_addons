# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    num_word = fields.Char(string="Amount In Words:", compute='_compute_amount_in_word')

    def _compute_amount_in_word(self):
        for rec in self:
            rec.num_word = str(rec.currency_id.amount_to_text(round(rec.amount_total))) + ' only'
