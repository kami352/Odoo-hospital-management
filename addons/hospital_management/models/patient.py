from odoo import fields, models, api

class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'

    name = fields.Char(string='Name', required=True)  # keep required=True
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')

    # Photo fields
    image = fields.Image(
        string='Photo',
        max_width=512,
        max_height=512,
        verify_resolution=False
    )
    image_small = fields.Image(
        string='Photo Small',
        related='image',
        max_width=128,
        max_height=128,
        store=True
    )
    medical_history_ids = fields.One2many(
        'hospital.medical.history',
        'patient_id',
        string='Medical History'
    )

    # Contact & Address fields
    phone = fields.Char(string='Phone', help="Mobile or landline")
    mobile = fields.Char(string='Mobile')
    email = fields.Char(string='Email')
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street2')
    city = fields.Char(string='City')
    zip = fields.Char(string='ZIP')
    country_id = fields.Many2one('res.country', string='Country')

    # Appointments relation & count
    appointment_ids = fields.One2many(
        'hospital.appointment',
        'patient_id',
        string='Appointments'
    )
    appointment_count = fields.Integer(
        string="Appointments",
        compute='_compute_appointment_count',
        store=True
    )

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for patient in self:
            patient.appointment_count = len(patient.appointment_ids)

    def action_view_appointments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }