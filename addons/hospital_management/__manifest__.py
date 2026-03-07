{
    'name': 'Hospital Management',
    'version': '18.0.1.0.0',
    'summary': 'Simple Hospital Management System',
    'description': 'Manage patients, doctors, and appointments in Odoo.',
    'category': 'Healthcare',
    'author': 'Your Name',
    'depends': ['base'],  # Depends on Odoo's base module (always needed).
    'data': [
    'security/ir.model.access.csv',
    'views/patient_views.xml',
    'views/doctor_views.xml',
    'views/appointment_views.xml',
    'views/department_views.xml',
   'reports/appointment_report.xml',
    'views/menu.xml',
],
    'installable': True,
    'application': True,
    'auto_install': False,
}