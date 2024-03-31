from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import re


class InheritedResPartner(models.Model):
    _inherit = "res.partner"

    @api.constrains('phone')
    def validate_phone_number(self):
        if not self.phone:
            raise ValidationError(_('Please enter phone number.'))
        pattern = re.compile(r'^\+(?:[0-9] ?){6,14}[0-9]$')
        if not re.match(pattern, self.phone):
            raise ValidationError(
                _('Invalid phone number. Try maximum 15 digit having the country code like this: +671 123 456 7890, +6711234567890'))

    @api.constrains('email')
    def validate_email(self):
        if not self.email:
            raise ValidationError(_('Please enter email address.'))
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not re.match(pattern, self.email):
            raise ValidationError(_('Invalid email address. Please provide a valid email address.'))
