from odoo import fields, models, api

class MedicalHistory(models.Model):
    _name = 'hospital.medical.history'
    _description = 'Patient Medical History'
    _order = 'date desc'

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True, ondelete='cascade')
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    diagnosis = fields.Text(string='Diagnosis')
    treatment = fields.Text(string='Treatment / Medication')
    notes = fields.Text(string='Additional Notes')
    allergy = fields.Boolean(string='Allergy / Reaction')
    allergy_description = fields.Text(string='Allergy Details', help="Describe any allergies or adverse reactions")

    @api.model
    def create(self, vals):
        # Optional: auto-set doctor to current user if doctor
        if not vals.get('doctor_id'):
            current_user = self.env.user
            doctor = self.env['hospital.doctor'].search([('user_id', '=', current_user.id)], limit=1)
            if doctor:
                vals['doctor_id'] = doctor.id
        return super(MedicalHistory, self).create(vals)