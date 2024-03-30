# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _compute_amount_in_word(self):
        for rec in self:
            rec.num_word = str(rec.currency_id.amount_to_text(rec.amount_total)) + ' only'

    num_word = fields.Char(string="Amount In Words:", compute='_compute_amount_in_word')
    items = fields.Text(string="Items")
    #client_lpo_no = fields.Char(string="ACE Quote Ref No./Client LPO No")
    project_id = fields.Many2one("project.project", string="Project Details")
    client_lpo_no = fields.Char(string="ACE Quote Ref No./Client LPO No", related="project_id.client_lpo_no")
    # project_ref = fields.Text(string="Project Reference")
    project_ref = fields.Char(string="Project Reference", related="project_id.project_location")
    delivery_terms = fields.Text(string="Terms Of Delivery")


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange("product_uom")
    def _onchange_product_uom(self):
        """
        Change domain of product_uom field
        """
        return {"domain": {"product_uom": []}}
