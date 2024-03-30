# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _compute_amount_in_word(self):
        for rec in self:
            rec.num_word = str(rec.currency_id.amount_to_text(rec.amount_total)) + ' only'

    num_word = fields.Char(string="Amount In Words:", compute='_compute_amount_in_word')
    sale_id = fields.Many2one("sale.order", string="Sale Order", compute="compute_order_id")
    purchase_id = fields.Many2one("purchase.order", string="Purchase Order", compute="compute_order_id")
   # client_lpo_no = fields.Char(string="ACE Quote Ref No./Client LPO No")
   # bill_client_lpo_no = fields.Char(string="ACE Quote Ref No./Client LPO No")
    items = fields.Text(string="Items")
    bill_items = fields.Text(string="Items")
    project_id = fields.Many2one("project.project", string="Project Details")
    client_lpo_no = fields.Char(string="ACE Quote Ref No./Client LPO No", related="project_id.client_lpo_no")
    bill_client_lpo_no = fields.Char(string="ACE Quote Ref No./Client LPO No", related="project_id.client_lpo_no")
    project_ref = fields.Char(string="Project Reference", related="project_id.project_location")
    bill_project_id = fields.Many2one("project.project", string="Project Details")
    bill_project_ref = fields.Char(string="Project Reference", related="bill_project_id.project_location")

    @api.depends("partner_id")
    def compute_order_id(self):
        """
        Set sale order with respect to invoice
        """
        self.sale_id = False
        self.purchase_id = False
        if not isinstance(self.id, models.NewId):
            for record in self:
                record.sale_id = False
                record.purchase_id = False
                sale_order = record.env["sale.order"].search([('invoice_ids', 'in', [record.id])])
                purchase_order = record.env["purchase.order"].search([('invoice_ids', 'in', [record.id])])
                if sale_order:
                    record.sale_id = sale_order.id
                    record.project_id = sale_order.project_id.id
                    #record.client_lpo_no = sale_order.client_lpo_no
                    #record.project_ref = sale_order.project_ref
                    record.items = sale_order.items
                if purchase_order:
                    record.purchase_id = purchase_order.id
                    record.bill_project_id = purchase_order.project_id.id
                    #record.bill_client_lpo_no = purchase_order.client_lpo_no
                    #record.bill_project_ref = purchase_order.project_ref
                    record.bill_items = purchase_order.items


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    freeze = fields.Boolean()
    lpo_no = fields.Char(string="Client LPO No", compute='compute_client_lpo_no', store=True)
    project_ref = fields.Char(string="Project Reference", related="move_id.project_ref", store=True)
    previous_price_unit = fields.Float(string='Previous Unit Price', digits='Product Price')
    previous_vat_amount = fields.Float(string='Previous VAT Amount', digits='Product Price')
    previous_subtotal = fields.Float(string='Previous Subtotal', digits='Product Price')

    @api.onchange('freeze')
    def _onchange_freeze(self):
        for line in self:
            if line.price_unit:
                line.previous_price_unit = line.price_unit
            if line.l10n_ae_vat_amount:
                line.previous_vat_amount = line.l10n_ae_vat_amount
            if line.price_subtotal:
                line.previous_subtotal = line.price_subtotal
            if line.freeze:
                line.price_unit = 0.00
                line._onchange_price_subtotal()
            else:
                line.price_unit = line.previous_price_unit
                line._onchange_price_subtotal()

    @api.depends('move_id.client_lpo_no', 'move_id.bill_client_lpo_no')
    def compute_client_lpo_no(self):
        for rec in self:
            rec.lpo_no = ''
            if rec.move_id.client_lpo_no:
                rec.lpo_no = rec.move_id.client_lpo_no
            if rec.move_id.bill_client_lpo_no:
                rec.lpo_no = rec.move_id.bill_client_lpo_no


    @api.onchange("product_uom_id")
    def _onchange_product_uom(self):
        """
        Change domain of product_uom field
        """
        return {"domain": {"product_uom_id": []}}





