from odoo import fields, models
from odoo.exceptions import ValidationError

class AppointmentCancelWizard(models.TransientModel):
    _name = 'hospital.appointment.cancel.wizard'
    _description = 'Cancel Appointment Wizard'

    appointment_id = fields.Many2one('hospital.appointment', required=True)
    reason = fields.Text(string='Cancellation Reason', required=True)

    def action_confirm_cancel(self):
        self.ensure_one()
        if not self.reason:
            raise ValidationError("Please provide a cancellation reason.")
        
        self.appointment_id.write({
            'state': 'cancel',
            'cancel_reason': self.reason,
            'cancelled_by_id': self.env.user.id,
            'cancelled_date': fields.Datetime.now(),
        })
        return {'type': 'ir.actions.act_window_close'}