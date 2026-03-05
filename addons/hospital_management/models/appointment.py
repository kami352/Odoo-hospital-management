from odoo import fields, models, api

class Appointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _rec_name = 'reference'
    _order = 'date desc'

    reference = fields.Char(string='Reference', default='New', readonly=True)
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now)

    # Add inside Appointment class
    department_id = fields.Many2one(
    'hospital.department',
    string='Department',
    related='doctor_id.department_id',
    store=True,           # optional: store for searching/filtering
    readonly=True
)  
    notes = fields.Text(string='Notes')


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