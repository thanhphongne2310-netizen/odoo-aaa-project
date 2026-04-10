{
    'name': 'AAA HR Management',
    'version': '1.0',
    'depends': ['base', 'hr', 'mail'], # Quan trọng: Phải có 'mail' để làm thông báo
    'data': [
        'security/ir.model.access.csv',
        'views/hr_request_views.xml',
    ],
    'installable': True,
    'application': True,
}