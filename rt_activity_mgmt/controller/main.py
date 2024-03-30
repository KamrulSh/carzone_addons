import odoo.http as http
from odoo.http import request

class BroadcastingStateController(http.Controller):

    @http.route('/broadcasting/<string:state>', type='http', auth="user")
    def broadcasting_state(self, state, **kwargs):
        if state == "today":
            return request.redirect('/web#action=rt_activity_mgmt.mail_activity_today_action')
        if state == "week":
            return request.redirect('/web#action=rt_activity_mgmt.mail_activity_week_action')
        if state == "month":
            return request.redirect('/web#action=rt_activity_mgmt.mail_activity_month_action')
        if state == "next_year":
            return request.redirect('/web#action=rt_activity_mgmt.mail_activity_next_year_action')
        if state == "overdue":
            return request.redirect('/web#action=rt_activity_mgmt.mail_activity_overdue_action')
        if state == "planned":
            return request.redirect('/web#action=rt_activity_mgmt.mail_activity_planned_action')

        return request.redirect('/web#action=rt_activity_mgmt.mail_activity_action')
