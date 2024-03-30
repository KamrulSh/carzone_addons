# -*- coding: utf-8 -*-
import datetime
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class AccountInvoice(models.Model):
    _inherit = "account.move"
    _description = "Account Move Paid Amounts"

    paid_amount = fields.Monetary(string='Paid Amount', compute='_compute_paid_amount', store=True, help="Paid Amount.")

    @api.depends('amount_residual')
    def _compute_paid_amount(self):
        for inv in self:
            inv.paid_amount = 0.0
            if inv.state != 'draft':
                inv.paid_amount = inv.amount_total - inv.amount_residual
                
                
class Partner(models.Model):
    _inherit = "res.partner"
    @api.depends('cust_acc_stat_line_ids','cust_acc_stat_line_ids.invoice_date_due','cust_acc_stat_line_ids.amount_residual')
    def _get_cust_amounts_and_date(self):
        company = self.env.user.company_id
        current_date = fields.Date.today()
        for partner in self:
            due_date = False
            amount_due = amount_overdue = 0.0
            for aml in partner.cust_acc_stat_line_ids:
                due_date = aml.invoice_date_due
                if (aml.company_id == company):
                    if not due_date:
                        due_date = aml.date or aml.invoice_date
                    amount_due += aml.amount_residual
                    if (due_date <= current_date):
                        amount_overdue += aml.amount_residual
            partner.cust_overall_balance_due = amount_due
            partner.cust_total_overdue_amount = amount_overdue
    
    @api.depends('supp_acc_stat_line_ids','supp_acc_stat_line_ids.invoice_date_due','supp_acc_stat_line_ids.amount_residual')
    def _get_supp_amounts_and_date(self):
        company = self.env.user.company_id
        current_date = fields.Date.today()
        for partner in self:
            due_date = False
            amount_due = amount_overdue = 0.0
            for aml in partner.supp_acc_stat_line_ids:
                due_date = aml.invoice_date_due
                if (aml.company_id == company):
                    amount_due += aml.amount_residual
                    if not due_date:
                        due_date = aml.date or aml.invoice_date
                    if (due_date <= current_date):
                        amount_overdue += aml.amount_residual
            partner.supp_overall_balance_due = amount_due
            partner.supp_total_overdue_amount = amount_overdue
            
    cust_acc_stat_line_ids = fields.One2many("account.move", "partner_id", string="Customer Account Statement", auto_join=True, domain=[('state','=','posted'),('move_type', 'in', ['out_invoice', 'out_refund', 'out_receipt'])])
    supp_acc_stat_line_ids = fields.One2many("account.move", "partner_id", string="Supplier Account Statement", auto_join=True, domain=[('state','=','posted'),('move_type','in',['in_invoice', 'in_refund','in_receipt'])])
    
    cust_overall_balance_due = fields.Float(compute='_get_cust_amounts_and_date')
    cust_total_overdue_amount = fields.Float(compute='_get_cust_amounts_and_date')
    
    supp_overall_balance_due = fields.Float(compute='_get_supp_amounts_and_date')
    supp_total_overdue_amount = fields.Float(compute='_get_supp_amounts_and_date')

    def do_print_cust_due_state(self):
        return self.env.ref('of_account_statement.action_report_customer_overdue_report').sudo().report_action(self.id)
    def do_print_cust_state(self):
        return self.env.ref('of_account_statement.action_report_customer_statement_report').sudo().report_action(self.id)
    
    def do_print_supp_due_state(self):
        return self.env.ref('of_account_statement.action_report_supplier_overdue_report').sudo().report_action(self.id)
    def do_print_supp_state(self):
        return self.env.ref('of_account_statement.action_report_supplier_statement_report').sudo().report_action(self.id)

    def action_cust_due_send(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        template_id =self.env.ref('of_account_statement.mail_template_cust_overdue').id
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'res.partner',
            'default_res_id' : self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode' : 'comment',
            'force_email' : True
        }

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }


    def action_cust_state_send(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        template_id =self.env.ref('of_account_statement.mail_template_cust_statement').id
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'res.partner',
            'default_res_id' : self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode' : 'comment',
            'force_email' : True
        }

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }


    def action_supp_state_send(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        template_id =self.env.ref('of_account_statement.mail_template_supp_statement').id
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'res.partner',
            'default_res_id' : self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode' : 'comment',
            'force_email' : True
        }

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
