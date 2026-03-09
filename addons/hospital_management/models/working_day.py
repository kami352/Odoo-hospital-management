from odoo import fields, models

class WorkingDay(models.Model):
    _name = 'hospital.working.day'
    _description = 'Working Day'
    _order = 'sequence'

    name = fields.Char(string='Day Name', required=True)
    sequence = fields.Integer(default=10)