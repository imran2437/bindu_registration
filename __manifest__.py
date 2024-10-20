{
    'name': 'Bindu Registration',
    'version': '1.0',
    'summary': 'User Registration for Bindu Get Together',
    'description': 'Allows users to register for the Bindu Get Together program and handle payments and invoices.',
    'author': 'Your Name',
    'category': 'Website',
    'depends': ['base', 'website', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        ## report
        'reports/report_action.xml',
        'reports/report_prescription_order.xml',
        
        'views/bindu_registration_template.xml',
        'views/bindu_registration_views.xml',
        
        
    ],
    'installable': True,
    'application': True,
}
