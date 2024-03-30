# -*- coding: utf-8 -*-

import pytz
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]

class MailActivity(models.Model):
    _inherit = "mail.activity"
    
    rt_activity_mgmt_color = fields.Integer('Color Index', default=0)    
    rt_activity_mgmt_priority = fields.Selection(
        AVAILABLE_PRIORITIES, string='Priority', index=True,
        default=AVAILABLE_PRIORITIES[0][0])    
    
    rt_activity_mgmt_tag_ids = fields.Many2many(
        comodel_name='rt_activity_mgmt.mail.activity.tag', relation='rt_activity_mgmt_activity_tag_rel', string='Tags',
       )

    state = fields.Selection(selection_add=[('today',), ('week', 'Week'),
                                            ('month', 'Month'), ('next_year', 'Next Year'),
                                            ('overdue',),('planned',)])
    broadcasting_summary = fields.Text(string='Service Details')

    @api.model
    def _compute_state_from_date(self, date_deadline, tz=False):
        date_deadline = fields.Date.from_string(date_deadline)
        today_default = date.today()
        today = today_default
        if tz:
            today_utc = pytz.utc.localize(datetime.utcnow())
            today_tz = today_utc.astimezone(pytz.timezone(tz))
            today = date(year=today_tz.year, month=today_tz.month, day=today_tz.day)
        diff = (date_deadline - today)
        if diff.days == 7:
            return 'week'
        elif diff.days in [30, 31]:
            return 'month'
        elif diff.days in [365, 366]:
            return 'next_year'
        else:
            return super()._compute_state_from_date(date_deadline, tz=tz)

    def action_rt_activity_mgmt_activity_edit(self):
        self.ensure_one()
        return {
            'name': self.display_name,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.activity',
            'res_id': self.id,
            'target': 'new',        
        }        
        
    def action_rt_activity_mgmt_activity_document(self):  
        self.ensure_one()
        print("\n\n self.res_id ==>",self.res_id)
        print("\n\n self.res_model ==>",self.res_model)        
        if self.res_id and self.res_model:
            domain = [['id','=',self.res_id]]
            return {
                'type': 'ir.actions.act_window',
                'name': self.res_model_id.sudo().name if self.res_model_id else '',
                'res_model': self.res_model,
                'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],  
                'search_view_id': [False],     
                'domain': domain,          
            }
        else:
            raise ValidationError(_('Document model or document id does not exist!'))              
                   
    
    @api.model
    def rt_activity_mgmt_retrieve_dashboard(self, domain=[]):
        """ This function returns the values to populate the custom dashboard in
            the activity views.
        """
        self.check_access_rights('read')
         
        result = {
            'all_state_today': 0,
            'all_state_week': 0,
            'all_state_month': 0,
            'all_state_next_year': 0,
            'all_state_overdue': 0,
            'all_state_planned': 0,
            'total': 0,
            'list_overview_activity_type':[],
        }
        
        
        activities = self.env['mail.activity'].search(domain)        
        total_activities = self.env['mail.activity'].search_count([])
        result['total'] = total_activities

        today = fields.Date.context_today(self)        
        result['all_state_today'] = len(activities.filtered(lambda a: a.date_deadline == today).ids)
        result['all_state_week'] = len(activities.filtered(lambda a: a.date_deadline == today + timedelta(days=7)).ids)
        result['all_state_month'] = len(activities.filtered(lambda a: a.date_deadline == today + timedelta(days=30)).ids)
        result['all_state_next_year'] = len(activities.filtered(lambda a: a.date_deadline == today + timedelta(days=366)).ids)
        result['all_state_overdue'] = len(activities.filtered(lambda a: a.date_deadline < today).ids)
        result['all_state_planned'] = len(activities.filtered(
            lambda a: a.date_deadline > today and a.date_deadline != today + timedelta(days=7) and a.date_deadline != today + timedelta(days=30)  and a.date_deadline != today + timedelta(days=366)).ids)
                 
        activity_type_ids = activities.mapped('activity_type_id')
        list_overview_activity_type = []
        if activity_type_ids:
            for activity_type_id in activity_type_ids:
                dic_activity_type_overview={
                'activity_type_name':activity_type_id.name,
                'overdue':len(activities.filtered(lambda a: a.date_deadline < today and a.activity_type_id == activity_type_id).ids),
                'today':len(activities.filtered(lambda a: a.date_deadline == today and a.activity_type_id == activity_type_id).ids),
                'week':len(activities.filtered(lambda a: a.date_deadline == today + timedelta(days=7) and a.activity_type_id == activity_type_id).ids),
                'month':len(activities.filtered(lambda a: a.date_deadline == today + timedelta(days=30) and a.activity_type_id == activity_type_id).ids),
                'next_year':len(activities.filtered(lambda a: a.date_deadline == today + timedelta(days=366) and a.activity_type_id == activity_type_id).ids),
                'planned':len(activities.filtered(lambda a: a.date_deadline > today and a.date_deadline != today + timedelta(days=7) and a.date_deadline != today + timedelta(days=30)  and a.date_deadline != today + timedelta(days=366) and a.activity_type_id == activity_type_id).ids),
                }
                list_overview_activity_type.append(dic_activity_type_overview)
        result['list_overview_activity_type'] = list_overview_activity_type        
        return result   
