from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import timedelta

class Appointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _rec_name = 'reference'
    _order = 'date desc'

    reference = fields.Char(string='Reference', default='New', readonly=True)
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    department_id = fields.Many2one(
        'hospital.department',
        string='Department',
        related='doctor_id.department_id',
        store=True,
        readonly=True
    )
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    notes = fields.Text(string='Notes')
    prescription = fields.Html(
        string='Prescription',
        help="Doctor's prescription or medication instructions"
    )
    treatment_notes = fields.Html(string='Treatment Notes')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True)

    cancel_reason = fields.Text(string='Cancellation Reason')
    cancelled_by_id = fields.Many2one('res.users', string='Cancelled By', readonly=True)
    cancelled_date = fields.Datetime(string='Cancelled On', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('reference', 'New') == 'New':
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or 'New'
        return super(Appointment, self).create(vals)

    # Workflow methods – now with permission check BEFORE write
    def action_confirm(self):
        if not self.env.user.can_set_confirmed:
            raise ValidationError(
                "You are not allowed to set appointments to 'Confirmed' status.\n"
                "Contact your administrator to update your permissions."
            )
        self.write({'state': 'confirmed'})
        return True

    def action_done(self):
        if not self.env.user.can_set_done:
            raise ValidationError(
                "You are not allowed to set appointments to 'Done' status.\n"
                "Contact your administrator to update your permissions."
            )
        self.write({'state': 'done'})
        return True

    def action_cancel(self):
        if not self.env.user.can_set_cancel:
            raise ValidationError(
                "You are not allowed to set appointments to 'Cancelled' status.\n"
                "Contact your administrator to update your permissions."
            )
        self.write({'state': 'cancel'})
        return True

    def action_draft(self):
        if not self.env.user.can_set_draft:
            raise ValidationError(
                "You are not allowed to set appointments to 'Draft' status.\n"
                "Contact your administrator to update your permissions."
            )
        self.write({'state': 'draft'})
        return True

    @api.constrains('date', 'doctor_id')
    def _check_doctor_availability(self):
        for appointment in self:
            if not appointment.doctor_id or not appointment.date:
                continue

            doctor = appointment.doctor_id
            appointment_date = appointment.date
            appointment_weekday = appointment_date.weekday()  # 0 = Monday

            day_map = {
                0: 'Monday',
                1: 'Tuesday',
                2: 'Wednesday',
                3: 'Thursday',
                4: 'Friday',
                5: 'Saturday',
                6: 'Sunday'
            }
            day_name = day_map.get(appointment_weekday)

            # Check if doctor works on this day
            if not doctor.working_day_ids.filtered(lambda d: d.name == day_name):
                raise ValidationError(
                    f"Doctor {doctor.name} does not work on {day_name}."
                )

            # Time check
            appointment_hour = appointment_date.hour + appointment_date.minute / 60.0

            if not (doctor.start_time <= appointment_hour <= doctor.end_time):
                raise ValidationError(
                    f"Appointment time is outside doctor's working hours "
                    f"({doctor.start_time} - {doctor.end_time})."
                )

            # Break time check
            if doctor.break_start and doctor.break_end:
                if doctor.break_start <= appointment_hour <= doctor.break_end:
                    raise ValidationError(
                        f"Appointment time overlaps doctor's break "
                        f"({doctor.break_start} - {doctor.break_end})."
                    )

            # Double-booking check (rough 1-hour window)
            overlapping = self.search([
                ('doctor_id', '=', doctor.id),
                ('date', '>=', appointment_date - timedelta(hours=1)),
                ('date', '<=', appointment_date + timedelta(hours=1)),
                ('id', '!=', appointment.id),
            ])

            if overlapping:
                raise ValidationError(
                    f"Doctor {doctor.name} already has an appointment at this time."
                )

    # Safety net for manual state changes (dropdown)
    @api.constrains('state')
    def _check_user_can_change_state(self):
        for appointment in self:
            user = self.env.user
            old_state = appointment._origin.state if appointment._origin else 'draft'
            new_state = appointment.state

            if new_state == old_state:
                continue

            permission_map = {
                'draft': 'can_set_draft',
                'confirmed': 'can_set_confirmed',
                'done': 'can_set_done',
                'cancel': 'can_set_cancel',
            }

            permission_field = permission_map.get(new_state)

            if permission_field and not getattr(user, permission_field, False):
                raise ValidationError(
                    f"You are not allowed to change appointment status to '{new_state}'.\n"
                    f"Contact your administrator to update your permissions."
                )