from odoo import fields, api, models, _
from datetime import datetime

from odoo.exceptions import UserError


class CreateUserEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def create(self, vals):
        emp_rec = super(CreateUserEmployee, self).create(vals)
        user_partner_id = self.env['hr.applicant'].sudo().browse(emp_rec.applicant_id.id).partner_id.id
        user_info = {'name': vals.get('name'),
                     'login': vals.get('work_email'),
                     'email': vals.get('work_email'),
                     'state': 'active',
                     'partner_id': user_partner_id if user_partner_id else None}
        rec = self.env['res.users'].sudo().create(user_info)
        emp_rec.user_id = rec.id
        return emp_rec


class HrApplicantInherit(models.Model):
    _inherit = 'hr.applicant'

    # work_email = fields.Char(string='Work email')

    def create_employee_from_applicant(self):
        # for applicant in self:
        #     contact_name = False
        #     # if applicant.partner_id:
        #     #     address_id = applicant.partner_id.address_get(['contact'])['contact']
        #     #     contact_name = applicant.partner_id.display_name
        #     if not applicant.partner_id:
        #         if not applicant.partner_name:
        #             raise UserError(_('You must define a Contact Name for this applicant.'))
        #         new_partner_id = self.env['res.partner'].create({
        #             'is_company': False,
        #             'type': 'private',
        #             'name': applicant.partner_name,
        #             'email': applicant.work_email,
        #             'phone': applicant.partner_phone,
        #             'mobile': applicant.partner_mobile
        #         })
        #         applicant.partner_id = new_partner_id
        #         address_id = new_partner_id.address_get(['contact'])['contact']
            res = super(HrApplicantInherit, self).create_employee_from_applicant()
            res['context']['default_work_email'] = None

            return res

