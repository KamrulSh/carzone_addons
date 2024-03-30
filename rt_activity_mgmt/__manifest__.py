# -*- coding: utf-8 -*-

{
    "name": "Activity Management | Activity Dashboard | Activity Monitoring | Activity Views",
    "version":"15.0.1",
    "license": "OPL-1",
    "support": "relief.4technologies@gmail.com",  
    "author" : "Relief Technologies",  
    "live_test_url": "https://youtu.be/p93lhTYTMOI",       
    "category": "Activity Management/Activity",
    "summary": "schedule activity management Mail Activity Board daily to do management to do list crm activity management sale activity management",
    "description": """

    """,
    "depends": ["base","mail"],
    "data": [
        "security/activity_security.xml",        
        "security/ir.model.access.csv",
        "views/activity_tag.xml",
        "views/mail_activity.xml",

    ],
    'assets': {
        'web.assets_backend': [
            'rt_activity_mgmt/static/src/scss/dashboard.scss',
            'rt_activity_mgmt/static/src/js/dashboard.js',
        ],
        'web.assets_qweb': [
            'rt_activity_mgmt/static/src/xml/**/*',
        ],
    },     
     
         
    "images": ["static/description/background.png",],              
    "installable": True,
    "application": True,
    "auto_install": False,
    "price": 35,
    "currency": "EUR"   
}
