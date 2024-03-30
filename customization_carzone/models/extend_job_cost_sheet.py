from odoo import models, fields, api
from odoo.exceptions import ValidationError


class JobCostSheet(models.Model):
    _inherit = "job.cost.sheet"

    cost_type = fields.Selection(
        [('material', 'Material'),
         ('overhead', 'Overhead'),
         ('labour', 'Labour'),
         ('sublet', 'Sublet')
         ],
        string='Type',
        default='material',
    )
    cc_sale_price = fields.Float(string="Sale Price")
    cc_check_box = fields.Boolean(string="Check", default=True)
    cc_account_move_line_id = fields.Many2one(string="Bill Line ID")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        rtn = super(JobCostSheet, self)._onchange_product_id()
        self.invoice_line_tax_ids = self.product_id.taxes_id.ids
        return rtn

    @api.onchange('cost_type')
    def onchange_cost_type(self):
        invoice_line_obj = self.env['account.move.line']
        for rec in self:
            if rec.cost_type == "sublet":
                sublet_obj = invoice_line_obj.search([('move_id.cc_job_card', '=', rec.id),('parent_state', '!=', 'cancel')])
                if sublet_obj:
                    if len(sublet_obj) == 1:
                        rec.cc_sale_price = sublet_obj.cc_sale_price
                    else:
                        raise ValidationError("Multiple Values Found for the same Job Card")
