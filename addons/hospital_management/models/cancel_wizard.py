from odoo import fields, models
from odoo.exceptions import ValidationError

class AppointmentCancelWizard(models.TransientModel):
    _name = 'hospital.appointment.cancel.wizard'
    _description = 'Cancel Appointment Wizard'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment', required=True)
    reason = fields.Text(string='Cancellation Reason', required=True)

    def action_confirm_cancel(self):
        self.ensure_one()

        # IMPORTANT: Check permission BEFORE doing anything
        if not self.env.user.can_set_cancel:
            raise ValidationError(
                "You are not allowed to cancel appointments.\n"
                "Contact your administrator to update your permissions."
            )

        # Check reason is filled
        if not self.reason or not self.reason.strip():
            raise ValidationError("Please provide a cancellation reason.")

        # If permission OK → cancel
        self.appointment_id.write({
            'state': 'cancel',
            'cancel_reason': self.reason.strip(),
            'cancelled_by_id': self.env.user.id,
            'cancelled_date': fields.Datetime.now(),
        })

        return {'type': 'ir.actions.act_window_close'}