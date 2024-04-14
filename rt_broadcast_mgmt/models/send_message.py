# -*- coding: utf-8 -*-
import urllib.parse as parse
import html2text
from lxml import etree
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class WhatsappEmailDelivered(models.Model):
    _name = 'whatsapp.email.delivered'
    _rec_name = 'customer_id'
    _order = 'sent_date desc'

    msg_type = fields.Selection([('email', 'Email'), ('whatsapp', 'WhatsApp')], string="Message Type")
    customer_id = fields.Many2one('res.partner', string="Customer")
    whatsapp_no = fields.Char(string="WhatsApp Number")
    wapp_email = fields.Char(string="Whatsapp/Email")
    message = fields.Html(string="Message")
    sent_date = fields.Datetime(string="Sent Date")
    state = fields.Selection(
        [("today", "Today"), ("week", "Week"), ("month", "Month"), ("next_year", "Next Year"), ("overdue", "Overdue"),
         ("planned", "Planned")], string="State")

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):

        result = super(WhatsappEmailDelivered, self).fields_view_get(view_id=view_id, view_type=view_type,
                                                                     toolbar=toolbar,
                                                                     submenu=submenu)
        doc = etree.XML(result['arch'])

        for node in doc.xpath("//form"):
            node.set('create', "false")
            node.set('edit', "false")

        for node in doc.xpath("//tree"):
            node.set('create', "false")
            node.set('edit', "false")

        result['arch'] = etree.tostring(doc)
        return result


class InheritedMailActivity(models.Model):
    _inherit = 'mail.activity'

    def action_send_email_selected(self):
        email_from = self.env['ir.mail_server'].search([], limit=1).smtp_user
        if not email_from:
            raise ValidationError(_('Please add smtp server for sending email.'))
        for data in self:
            email_to = data.email
            body_html = data.whatsapp_data
            data_vals = {
                'msg_type': 'email',
                'customer_id': data.partner_id.id,
                'wapp_email': email_to,
                'message': body_html,
                'sent_date': fields.Datetime.now(),
                'state': data.state
            }
            self.env['whatsapp.email.delivered'].create(data_vals)

            email_vals = {
                'subject': 'Do maintenance of your vehicle with us',
                'email_from': email_from,
                'email_to': email_to,
                'body_html': body_html,
                'auto_delete': False,
            }
            mail_id = self.env['mail.mail'].sudo().create(email_vals)
            mail_id.sudo().send()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'sticky': True,
            'params': {
                'type': 'success',
                'message': _('Email sent successfully to all selected recipients.'),
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }

    def action_send_message_whatsapp(self):
        if not self.contact:
            raise ValidationError(_('Please add phone number to this customer.'))

        else:
            phone_no = self.contact.replace(" ", "").replace("-", "")
            txt_msg = html2text.html2text(self.whatsapp_data)
            data_vals = {
                'msg_type': 'whatsapp',
                'customer_id': self.partner_id.id,
                'wapp_email': self.contact,
                'message': self.whatsapp_data,
                'sent_date': fields.Datetime.now(),
                'state': self.state
            }
            self.env['whatsapp.email.delivered'].create(data_vals)
            self.env['mail.message'].create(
                {'body': f'Whatsapp Message sent to {self.contact}', 'message_type': 'comment',
                 'model': 'mail.activity', 'res_id': self.id})
            link = "https://web.whatsapp.com/send?phone=" + phone_no
            message_string = parse.quote(txt_msg)

            url_id = link + "&text=" + message_string
            return {
                'type': 'ir.actions.act_url',
                'url': url_id,
                'target': 'new',
                'res_id': self.id,
            }

    def action_send_message_email(self):
        email_from = self.env['ir.mail_server'].search([], limit=1).smtp_user
        email_to = self.email
        if not email_from:
            raise ValidationError(_('Please add smtp server for sending email.'))
        if not email_to:
            raise ValidationError(_('Please email address for sending email.'))
        data_vals = {
            'msg_type': 'email',
            'customer_id': self.partner_id.id,
            'wapp_email': email_to,
            'message': self.whatsapp_data,
            'sent_date': fields.Datetime.now(),
            'state': self.state
        }
        self.env['whatsapp.email.delivered'].create(data_vals)
        self.env['mail.message'].create(
            {'body': f'Email sent to {self.email}', 'message_type': 'comment',
             'model': 'mail.activity', 'res_id': self.id})

        email_vals = {
            'subject': 'Do maintenance of your vehicle with us',
            'email_from': email_from,
            'email_to': email_to,
            'body_html': self.whatsapp_data,
            'auto_delete': False,
        }
        mail_id = self.env['mail.mail'].sudo().create(email_vals)
        mail_id.sudo().send()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'sticky': True,
            'params': {
                'type': 'success',
                'message': _('Email sent successfully to the recipient.'),
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
