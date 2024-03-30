# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Customization Statement Details',
    'version' : '5.0.0.2',
    'summary': 'Customization Statement Details',
    'sequence': 10,
    'description': """
    """,
    'category': 'Other',
    'website': 'https://www.odoo.com/app/invoicing',
    'images' : [],
    'depends' : ['base','of_account_statement','formatted_reports'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/contact_form_view_extend.xml',
        'views/report_cust_acc_stat.xml',
        'views/extend_project_project.xml',
        # 'views/extend_work_order.xml',
        
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {
        'web._assets_primary_variables': [],
        'web.assets_backend': [],
        'web.assets_frontend': [],
        'web.assets_tests': [],
        'web.qunit_suite_tests': [],
        'web.assets_qweb': [],
    },
    'license': 'LGPL-3',
}
