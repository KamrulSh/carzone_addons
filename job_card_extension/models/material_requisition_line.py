# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order.line'

    is_material_purchase_requisition_line = fields.Boolean(string="Is Material Purchase Requisition?")

class MaterialPurchaseRequisition(models.Model):
    _inherit = 'material.purchase.requisition'

    is_approved = fields.Boolean(string="Is Approved?")

    def user_approve(self):
        for rec in self:
            rec.userrapp_date = fields.Date.today()
            rec.approve_employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            rec.is_approved = True
            rec.state = 'approve'

            # create picking and remove products from inventory
            rec.request_stock()

    @api.model
    def _prepare_pick_vals(self, line=False, stock_id=False):
        pick_vals = super(MaterialPurchaseRequisition, self)._prepare_pick_vals(line, stock_id)
        pick_vals.update({
            'product_uom_qty': line.qty
        })
        return pick_vals

class MaterialPurchaseRequisitionLine(models.Model):
    _inherit = 'material.purchase.requisition.line'

    added_in_cost_sheet = fields.Boolean(string="Added in cost sheet")
    is_approved = fields.Boolean(related="requisition_id.is_approved", string="Is Approved")

    def action_requisition_approve(self):
        """
        Approve Material Requisition Lines
        """
        self.is_approved = True
        return True

    def action_add_line_in_cost_sheet(self):
        """
        Add requisition lines in cost sheet
        """
        job_cost_sheet = self.env['job.cost.sheet']
        account = self.product_id.product_tmpl_id.get_product_accounts(fiscal_pos=None)['income']
        job_cost_sheet.create({
            'cost_type': 'material',
            'product_id': self.product_id.id,
            'name': self.description,
            'quantity': self.qty,
            'uom_id': self.uom.id,
            'account_id': account.id,
            'price_unit': self.product_id.lst_price,
            'task_id': self.task_id.id

        })
        self.added_in_cost_sheet = True