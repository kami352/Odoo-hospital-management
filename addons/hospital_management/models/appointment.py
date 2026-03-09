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

    # Workflow methods called by buttons
    def action_confirm(self):
        self.write({'state': 'confirmed'})
        return True

    def action_done(self):
        self.write({'state': 'done'})
        return True

    def action_cancel(self):
        self.write({'state': 'cancel'})
        return True

    def action_draft(self):
        self.write({'state': 'draft'})
        return True

    @api.constrains('date', 'doctor_id')
    def _check_doctor_availability(self):
        for appointment in self:
            if not appointment.doctor_id or not appointment.date:
                continue

            doctor = appointment.doctor_id
            appointment_date = appointment.date
            appointment_weekday = appointment_date.weekday()  # 0 = Monday, 6 = Sunday

            # Map weekday number to day name
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

            # Check if doctor works on this day (using Many2many field)
            if not doctor.working_day_ids.filtered(lambda d: d.name == day_name):
                raise ValidationError(
                    f"Doctor {doctor.name} does not work on {day_name}."
                )

            # Convert appointment time to float hours
            appointment_hour = appointment_date.hour + appointment_date.minute / 60.0

            # Check working hours
            if not (doctor.start_time <= appointment_hour <= doctor.end_time):
                raise ValidationError(
                    f"Appointment time is outside doctor's working hours "
                    f"({doctor.start_time} - {doctor.end_time})."
                )

            # Check break time (if defined)
            if doctor.break_start and doctor.break_end:
                if doctor.break_start <= appointment_hour <= doctor.break_end:
                    raise ValidationError(
                        f"Appointment time overlaps doctor's break "
                        f"({doctor.break_start} - {doctor.break_end})."
                    )

            # Check double-booking (same doctor, overlapping time)
            overlapping = self.search([
                ('doctor_id', '=', doctor.id),
                ('date', '>=', appointment_date - timedelta(hours=1)),  # rough overlap check
                ('date', '<=', appointment_date + timedelta(hours=1)),
                ('id', '!=', appointment.id),
            ])

            if overlapping:
                raise ValidationError(
                    f"Doctor {doctor.name} already has an appointment at this time."
                )