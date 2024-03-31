from odoo import models, fields, api, _


class GarageBooking(models.Model):
    _name = 'garage.booking'
    _description = 'Garage Booking'
    _rec_name = 'customer_name'
    _order = 'create_date desc'

    customer_name = fields.Char(string='Customer Name', required=True)
    customer_email = fields.Char(string='Customer Email', required=True)
    customer_phone = fields.Char(string='Customer Phone', required=True)
    date_deadline = fields.Date(string='Date Deadline')
    planned_date = fields.Date(string='Planned Date')
    vehicle_no = fields.Char(string='Vehicle No')
    vehicle_model = fields.Char(string='Vehicle Model')
    chassis_no = fields.Char(string='Chassis No')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('broadcast', 'Broadcast')], string='Status',
                             default='draft')

    def action_confirm_booking(self):
        self.write({'state': 'confirm'})
        vehicle_model = self.env['vehicle.model'].search([('name', '=', self.vehicle_model)], limit=1)
        if not vehicle_model:
            self.env['vehicle.model'].create({'name': self.vehicle_model})
        vehicle_model_id = self.env['vehicle.model'].search([('name', '=', self.vehicle_model)], limit=1).id
        customer_data = {
            'name': self.customer_name,
            'phone': self.customer_phone,
            'email': self.customer_email,
            'company_type': 'person',
            'vehicle_no': self.vehicle_no,
            'model_id': vehicle_model_id,
            'chassis_no': self.chassis_no,
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

    def action_broadcast(self):
        self.write({'state': 'broadcast'})
        customer_id = self.env['res.partner'].search(
            [('name', '=', self.customer_name), ('phone', '=', self.customer_phone),
             ('email', '=', self.customer_email), ('vehicle_no', '=', self.vehicle_no)], limit=1)
        broadcast_data = {
            'partner_id': customer_id.id,
            'activity_type_id': 1,
            'date_deadline': self.date_deadline,
            'user_id': self.env.user.id,
            'vehicle_no': customer_id.vehicle_no,
            'model_id': customer_id.model_id.id,
            'chassis_no': customer_id.chassis_no,
        }
        self.env['mail.activity'].create(broadcast_data)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'sticky': True,
            'params': {
                'type': 'success',
                'message': _('Successfully added to the broadcasting.'),
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
