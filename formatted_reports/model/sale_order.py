# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _compute_amount_in_word(self):
        for rec in self:
            rec.num_word = str(rec.currency_id.amount_to_text(rec.amount_total)) + ' only'

    num_word = fields.Char(string="Amount In Words:", compute='_compute_amount_in_word')
    #client_lpo_no = fields.Char(string="ACE Quote Ref No./Client LPO No")
    # project_ref = fields.Text(string="Project Reference")
    items = fields.Text(string="Items")
    project_id = fields.Many2one("project.project", string="Project Details")
    project_ref = fields.Char(string="Project Reference", related="project_id.project_location")
    client_lpo_no = fields.Char(string="ACE Quote Ref No./Client LPO No", related="project_id.client_lpo_no")

    def _amount_all(self):
        res = super()._amount_all()
        for rec in self:
            total_amount = 0
            total_tax = 0
            for line in rec.order_line:
                if line.freeze:
                    total_amount = total_amount + line.price_subtotal
                    total_tax = total_tax + line.price_tax

            rec.amount_untaxed = rec.amount_untaxed - total_amount
            rec.amount_total = rec.amount_total - (total_amount + total_tax)
        return res

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    freeze = fields.Boolean()

    @api.onchange("product_uom")
    def _onchange_product_uom(self):
        """
        Change domain of product_uom field
        """
        return {"domain": {"product_uom": []}}

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        invoice_vals = self.super()._prepare_invoice_values(order, name, amount, so_line)
        if so_line.freeze:
            invoice_vals['invoice_line_ids'] = [(0, 0, {
                'freeze': so_line.freeze,
                'name': name,
                'price_unit': amount,
                'quantity': 1.0,
                'product_id': self.product_id.id,
                'product_uom_id': so_line.product_uom.id,
                'tax_ids': [(6, 0, so_line.tax_id.ids)],
                'sale_line_ids': [(6, 0, [so_line.id])],
                'analytic_tag_ids': [(6, 0, so_line.analytic_tag_ids.ids)],
                'analytic_account_id': order.analytic_account_id.id if not so_line.display_type and order.analytic_account_id.id else False,
            })]

        return invoice_vals

