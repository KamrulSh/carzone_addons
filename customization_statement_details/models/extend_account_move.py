from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"
    
    project_name = fields.Char(string="Project Number", related="project_id.name", store=True)
    project_location = fields.Char(string="Project Location", related="project_id.project_location", store=True)