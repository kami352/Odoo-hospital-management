from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    can_set_draft = fields.Boolean(
        string="Can set to Draft",
        default=True,
        help="Allow this user to set appointments to Draft status"
    )
    can_set_confirmed = fields.Boolean(
        string="Can set to Confirmed",
        default=True,
        help="Allow this user to set appointments to Confirmed status"
    )
    can_set_done = fields.Boolean(
        string="Can set to Done",
        default=False,
        help="Allow this user to set appointments to Done status"
    )
    can_set_cancel = fields.Boolean(
        string="Can set to Cancel",
        default=False,
        help="Allow this user to set appointments to Cancel status"
    )