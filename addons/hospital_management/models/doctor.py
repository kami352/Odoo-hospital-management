from odoo import fields, models, api

class Doctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctor'

    name = fields.Char(string='Name', required=True)
    specialty = fields.Char(string='Specialty')  # E.g., 'Cardiology'
    department_id = fields.Many2one('hospital.department', string='Department')

    # Multiple working days – Many2many
    working_day_ids = fields.Many2many(
        'hospital.working.day',
        string='Working Days',
        help="Select the days the doctor is available"
    )

    start_time = fields.Float(string='Start Time', default=9.0, help="In hours (e.g. 9.0 = 9:00 AM)")
    end_time = fields.Float(string='End Time', default=17.0, help="In hours (e.g. 17.0 = 5:00 PM)")
    break_start = fields.Float(string='Break Start', default=0.0, help="Optional break (0 = no break)")
    break_end = fields.Float(string='Break End', default=0.0)

    # Optional: computed field to show working days as text
    working_days_display = fields.Char(
        string='Working Days',
        compute='_compute_working_days_display',
        store=False
    )

    @api.depends('working_day_ids')
    def _compute_working_days_display(self):
        for doctor in self:
            days = doctor.working_day_ids.mapped('name')
            doctor.working_days_display = ", ".join(days) if days else "No days selected"