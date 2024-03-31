{
    'name': "Booking and Broadcasting management",

    'summary': """
        Broadcast whatsapp message and email and book for customer vehicle servicing""",

    'description': """
        Broadcast whatsapp message and email from tree view and form view and create booking information for customer vehicle
    """,

    'author': "Kamrul Islam Shahin",
    'website': "https://kamrulsh.github.io/",
    'category': 'Tools',
    'version': '15.0.0.1',

    'depends': ['base', 'mail', 'contacts', 'rt_activity_mgmt', 'website'],

    'data': [
        'data/general.xml',
        'security/ir.model.access.csv',
        'views/booking_form_template.xml',
        'views/garage_booking_views.xml',
        'views/send_message_views.xml',
        'views/broadcast_whatsapp_text.xml',
        'views/inherit_mail_activity.xml',
    ],
    'external_dependencies': {
        'python': ['html2text'],
    },
    'installable': True,
    'application': True,
    'sequence': 1,
    'auto_install': False,
}
