from odoo import fields, models, api
from odoo.exceptions import ValidationError  # ← ADD THIS LINE

class Appointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _rec_name = 'reference'
    _order = 'date desc'

    reference = fields.Char(string='Reference', default='New', readonly=True)
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now)

    cancel_reason = fields.Text(string='Cancellation Reason')
    cancelled_by_id = fields.Many2one('res.users', string='Cancelled By', readonly=True)
    cancelled_date = fields.Datetime(string='Cancelled On', readonly=True)

    prescription = fields.Html(string='Prescription')
    treatment_notes = fields.Html(string='Treatment Notes')

    # Add inside Appointment class
    department_id = fields.Many2one(
    'hospital.department',
    string='Department',
    related='doctor_id.department_id',
    store=True,           # optional: store for searching/filtering
    readonly=True
)  
    notes = fields.Text(string='Notes')

    prescription = fields.Html(
    string='Prescription',
    help="Doctor's prescription or medication instructions"
)


    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True)

    

    @api.model
    def create(self, vals):
        if vals.get('reference', 'New') == 'New':
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or 'New'
        return super(Appointment, self).create(vals)

    # ── NEW: Workflow methods called by buttons ──
    def action_confirm(self):
        self.write({'state': 'confirmed'})
        return True  # Return True to allow button action

    def action_done(self):
        self.write({'state': 'done'})
        return True

    def action_cancel(self):
        self.write({'state': 'cancel'})
        return True

    def action_draft(self):
        self.write({'state': 'draft'})
        return True
    
    