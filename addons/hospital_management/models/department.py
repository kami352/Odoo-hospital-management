from odoo import fields, models

class Department(models.Model):
    _name = 'hospital.department'
    _description = 'Hospital Department'
    _order = 'name'

    name = fields.Char(string='Department Name', required=True)
    code = fields.Char(string='Code', size=8)               # e.g. CARDIO, NEURO
    active = fields.Boolean(default=True)

    