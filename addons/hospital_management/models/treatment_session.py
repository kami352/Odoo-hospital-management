from odoo import fields, models, api

class TreatmentSession(models.Model):
    _name = 'hospital.treatment.session'
    _description = 'Treatment Session'
    _order = 'date desc'

    appointment_id = fields.Many2one(
    'hospital.appointment',
    string='Appointment',
    required=False,  # ← change to False
    ondelete='set null'  # if appointment deleted, keep session but clear link
)
    patient_id = fields.Many2one('hospital.patient', related='appointment_id.patient_id', store=True)
    doctor_id = fields.Many2one('hospital.doctor', related='appointment_id.doctor_id', store=True)
    date = fields.Datetime(related='appointment_id.date', store=True)
    treatment_type = fields.Selection([
        ('manual_therapy', 'Manual Therapy'),
        ('exercise_therapy', 'Exercise Therapy'),
        ('ultrasound', 'Ultrasound'),
        ('tens', 'TENS'),
        ('dry_needling', 'Dry Needling'),
        ('cupping', 'Cupping'),
        ('electrotherapy', 'Electrotherapy'),
        ('other', 'Other'),
    ], string='Treatment Type', required=True)
    duration_minutes = fields.Integer(string='Duration (minutes)', default=30)
    notes = fields.Text(string='Session Notes')
    pain_before = fields.Integer(string='Pain Before (0-10)')
    pain_after = fields.Integer(string='Pain After (0-10)')
    progress = fields.Selection([
        ('improved', 'Improved'),
        ('stable', 'Stable'),
        ('worsened', 'Worsened'),
    ], string='Progress')