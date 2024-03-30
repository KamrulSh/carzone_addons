from odoo import models, fields, api

class Project(models.Model):
    _inherit = "project.project"
    _order = "create_date desc"