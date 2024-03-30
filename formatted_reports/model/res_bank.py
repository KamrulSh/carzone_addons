# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResBank(models.Model):
    _inherit = 'res.bank'

    iban_no = fields.Char(string="IBAN NO.")