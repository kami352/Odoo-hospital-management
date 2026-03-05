from odoo import fields, models

class Doctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctor'

    name = fields.Char(string='Name', required=True)
    specialty = fields.Char(string='Specialty')  # E.g., 'Cardiology'.

    department_id = fields.Many2one(
        'hospital.department',
        string='Department'
    )