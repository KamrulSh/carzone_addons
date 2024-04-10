from odoo import models, fields, api


class InheritFleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    @api.model
    def create(self, vals):
        res = super(InheritFleetVehicle, self).create(vals)
        active_id = self.env.context.get('active_id')
        booking_mode = self.env.context.get('status')
        booking_id = self.env['garage.booking'].browse(active_id)
        if booking_mode == 'confirm':
            booking_id.write({
                'state': 'fleet',
            })
        return res
