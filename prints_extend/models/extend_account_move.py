import datetime

from odoo import models, fields, api
from num2words import num2words

class AccountMove(models.Model):
    _inherit = "account.move"

    excess_amount_move_id = fields.Many2one("account.move", string="Invoice Excess Amount", copy=False)
    partner_excess_amount = fields.Many2one("res.partner", string="Charged To", copy=False)
    excess_amount = fields.Monetary(string="Excess Amount", copy=False, readonly=1)
    cc_total_amount = fields.Monetary(string="Total Amount", compute="depends_invoice_line_ids", store=True)


    @api.depends('invoice_line_ids')
    def depends_invoice_line_ids(self):
        for rec in self:
            invoice_line_ids = rec.invoice_line_ids
            rec.excess_amount = sum(invoice_line_ids.mapped('discount_fixed'))
            rec.cc_total_amount = sum(invoice_line_ids.mapped('price_subtotal')) + rec.excess_amount

    def action_post(self):
        res = super(AccountMove, self).action_post()
        if self.excess_amount and self.partner_excess_amount:
            excess_amount_move_id = self.excess_amount_move_id
            invoice = None
            product_id = self.env['product.product'].search([('name', '=', 'Excess Amount'), ('default_code', '=', 'PEA')])
            vals = [{
                'product_id': product_id.id,
                'tax_ids': product_id.taxes_id.ids if product_id.taxes_id else "",
                'name': product_id.name,
                'quantity': 1,
                'price_unit': self.excess_amount,
            }]
            if excess_amount_move_id:
                excess_amount_move_id.invoice_line_ids = [(5,0,0)]
                excess_amount_move_id.update({
                    'partner_id': self.partner_excess_amount,
                    'cc_vehicle': self.cc_vehicle.id if self.cc_vehicle else "",
                })
                excess_amount_move_id.action_post()
            else:
                invoice = self.create({
                                    'partner_id': self.partner_excess_amount,
                                    'invoice_date': datetime.date.today(),
                                    'cc_vehicle': self.cc_vehicle.id if self.cc_vehicle else "",
                                    'invoice_line_ids': vals
                                })
                invoice.action_post()
                self.excess_amount_move_id = invoice.id

        return res

    def button_draft(self):
        res = super(AccountMove, self).button_draft()
        if self.excess_amount_move_id:
            self.excess_amount_move_id.button_draft()
            self.excess_amount_move_id.unlink()

        return res

    def num_convert_to_text(self, num):
        a = num2words(num)
        return a.upper()


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    discount_fixed = fields.Float(
        string="Excess Amount",
        digits="Product Price",
        default=0.00,
        help="Excess Amount",
    )