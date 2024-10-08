# -*- coding: utf-8 -*-

{
    'name': 'Odoo University Management App',
    "author": "Edge Technologies",
    'version': '15.0.1.1',
    'live_test_url': "https://youtu.be/5pUiOQZUghQ",
    "images":['static/description/main_screenshot.png'],
    'summary': 'University management education management system university education management school management system school education management class management system faculty management system exam management student management system',
    'description': "This app contain university management like student,faculty,assignment,admission,activity,exam etc.",
    "license" : "OPL-1",
    'depends': [
        'base',
        'account',
        'hr',
    ],
    'data': [
            'security/ir.model.access.csv',
            'data/sequence.xml',
            'views/university_student_view.xml',
            'views/university_course_view.xml',
            'views/university_batch_view.xml',
            'views/university_subject_view.xml',
            'views/university_faculty_view.xml',
            'views/university_admission_view.xml',
            'views/assignment_type_view.xml',
            'views/university_assignment_view.xml',
            'views/attendance_register_view.xml',
            'views/student_attendance_view.xml',
            'views/exam_type_view.xml',
            'views/exam_center_room_block_view.xml',
            'views/university_exam_view.xml',
            'views/parent_relationship_view.xml',
            'views/parent_student_view.xml',
            'views/result_template_view.xml',
            'views/student_marksheet_view.xml',
            'views/library_card_view.xml',
            'views/library_book_author_view.xml',
            'views/library_book_publisher_view.xml',
            'views/library_media_view.xml',
            'wizard/student_hall_ticket_view.xml',
            'report/student_hall_ticket_report_templates.xml',
            'report/report.xml',
            'wizard/admission_register_report_views.xml',
    ],
    'demo': [ ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 100,
    'currency': "EUR",
    'category': 'Industries',
}
