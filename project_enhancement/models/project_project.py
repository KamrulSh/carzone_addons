from odoo import fields, models


class Project(models.Model):
    _inherit = "project.project"

    project_location = fields.Char(string="Project Location")
    client_lpo_no = fields.Char(string="ACE Quote Ref No./Client LPO No")
