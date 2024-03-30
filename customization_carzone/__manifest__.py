# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

{
    'name': 'Carzone Customization',
    'version': '15.0.2.2.2',
    'category': 'Other',
    'live_test_url': 'https://www.ab.com',
    'summary': """ Carzone Customization""",
    'description': """
                    """,
    'author': 'Cybrosys Techno Solutions, Odoo SA',
    'website': "https://www.cybrosys.com",
    'company': 'Coders Cloud',
    'maintainer': 'Coders Cloud',
    'depends': ['base', 'job_card','fleet','hr_timesheet','project','garage_management_odoo','account',
                'web_tree_dynamic_colored_field'],
    'data': [
        'security/ir.model.access.csv',
        'views/extend_vehicle_form.xml',
        'views/extend_res_partner_form.xml',
        'views/extend_account_move.xml',
        'views/extend_project_task.xml',
        'views/extend_job_card_view_inherit_buttons.xml',

    ],
    'license': 'LGPL-3',
    'images': ['static/description/banner.gif'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
