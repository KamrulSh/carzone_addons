from odoo import api, fields, models


class Company(models.Model):
    _inherit = "res.company"

    report_header_image = fields.Binary(string="Report Header")
    report_footer_image = fields.Binary(string="Report Footer")


class Partner(models.Model):
    _inherit = "res.partner"

    trn_no = fields.Char(string="TRN No.")
