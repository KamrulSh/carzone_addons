import urllib.parse as parse
import html2text
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class GarageBooking(models.Model):
    _name = 'garage.booking'
    _description = 'Garage Booking'
    _rec_name = 'customer_name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']

    customer_name = fields.Char(string='Customer Name', required=True, tracking=True)
    customer_email = fields.Char(string='Customer Email', required=True, tracking=True)
    customer_phone = fields.Char(string='Customer Phone', required=True, tracking=True)
    booking_date = fields.Date(string='Booking Date', tracking=True)
    date_deadline = fields.Date(string='Date Deadline', tracking=True)
    planned_date = fields.Date(string='Planned Date', tracking=True)
    vehicle_no = fields.Char(string='Vehicle License No', required=True, tracking=True)
    vehicle_brand_id = fields.Many2one('fleet.vehicle.model.brand', string='Vehicle Brand', tracking=True)
    vehicle_model_id = fields.Many2one('fleet.vehicle.model', string='Vehicle Model', tracking=True)
    chassis_no = fields.Char(string='Chassis No', tracking=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'), ('fleet', 'Fleet'), ('broadcast', 'Broadcast')],
        string='Status', default='draft')
    is_new_customer = fields.Char(string='Is New Customer', readonly=True, store=True)
    whatsapp_data = fields.Html(string="Whatsapp Details", tracking=True)

    def action_confirm_booking(self):
        self.write({'state': 'confirm'})
        customer_vehicle = self.env['fleet.vehicle'].search([('license_plate', '=', self.vehicle_no)], limit=1)
        self.env['mail.message'].create(
            {'body': 'Booking confirmed.', 'message_type': 'comment',
             'model': 'garage.booking', 'res_id': self.id})
        if customer_vehicle:
            self.is_new_customer = 'No'

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'sticky': True,
                'params': {
                    'type': 'warning',
                    'message': _('This customer vehicle is already exist.'),
                    'next': {'type': 'ir.actions.act_window_close'},
                }
            }

        else:
            self.is_new_customer = 'Yes'
            customer_data = {
                'name': self.customer_name,
                'phone': self.customer_phone,
                'email': self.customer_email,
                'company_type': 'person',
            }
            self.env['res.partner'].create(customer_data)

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'sticky': True,
                'params': {
                    'type': 'success',
                    'message': _('Booking confirmed and created customer data.'),
                    'next': {'type': 'ir.actions.act_window_close'},
                }
            }

    def action_create_fleet(self):
        view = self.env.ref('fleet.fleet_vehicle_view_form')
        partner_id = self.env['res.partner'].search([('name', '=', self.customer_name),
                                                     ('phone', '=', self.customer_phone),
                                                     ('email', '=', self.customer_email)], limit=1)
        return {
            'name': _('Create Fleet Data'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'fleet.vehicle',
            'views': [(view.id, 'form')],
            'context': {
                'default_model_id': self.vehicle_model_id.id,
                'default_cc_partner': partner_id.id,
                'default_license_plate': self.vehicle_no,
                'default_vin_sn': self.chassis_no,
                'create': False,
                'status': 'confirm'
            },
            'target': 'new',
        }

    def action_broadcast(self):
        view = self.env.ref('mail.mail_activity_view_form_popup')
        customer_id = self.env['fleet.vehicle'].search([('license_plate', '=', self.vehicle_no)], limit=1)
        print('customer_id', customer_id, customer_id.license_plate)
        #
        return {
            'name': _('Create Broadcast'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.activity',
            'views': [(view.id, 'form')],
            'context': {
                'default_partner_id': customer_id.cc_partner.id,
                'create': False,
                'status': 'fleet'
            },
            'target': 'new',
        }

    def action_send_message(self):
        customer_id = self.env['res.partner'].search(
            [('phone', '=', self.customer_phone), ('email', '=', self.customer_email)], limit=1)
        if not self.customer_phone:
            raise ValidationError(_('Please add phone number to this customer.'))

        else:
            phone_no = self.customer_phone.replace(" ", "").replace("-", "")
            txt_msg = html2text.html2text(self.whatsapp_data)
            data_vals = {
                'msg_type': 'whatsapp',
                'customer_id': customer_id.id,
                'wapp_email': phone_no,
                'message': self.whatsapp_data,
                'sent_date': fields.Datetime.now(),
            }
            self.env['whatsapp.email.delivered'].create(data_vals)
            self.env['mail.message'].create(
                {'body': f'Whatsapp Message sent to {self.customer_phone}', 'message_type': 'comment',
                 'model': 'garage.booking', 'res_id': self.id})
            link = "https://web.whatsapp.com/send?phone=" + phone_no
            message_string = parse.quote(txt_msg)

            url_id = link + "&text=" + message_string
            return {
                'type': 'ir.actions.act_url',
                'url': url_id,
                'target': 'new',
                'res_id': self.id,
            }

    @api.onchange("booking_date", "date_deadline", "planned_date", "vehicle_no")
    def onchange_booking_whatsapp_text(self):
        company_name = self.env.company.name
        company_phone = self.env.company.phone

        for rec in self:
            whatsapp_template = self.env['booking.whatsapp.text'].search([], limit=1).text
            if whatsapp_template:
                formatted_whatsapp_data = whatsapp_template.format(
                    customer_name=rec.customer_name,
                    customer_email=rec.customer_email,
                    customer_phone=rec.customer_phone,
                    booking_date=rec.booking_date.strftime('%Y-%m-%d') if rec.booking_date else '',
                    date_deadline=rec.date_deadline.strftime('%Y-%m-%d') if rec.date_deadline else '',
                    planned_date=rec.planned_date.strftime('%Y-%m-%d') if rec.planned_date else '',
                    license_plate=rec.vehicle_no or '',
                    vehicle_model=rec.vehicle_model_id.name or '',
                    chassis_no=rec.chassis_no or '',
                    company_name=company_name or '',
                    company_phone=company_phone or '',
                )
                rec.whatsapp_data = formatted_whatsapp_data
