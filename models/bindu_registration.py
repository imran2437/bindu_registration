from odoo import models, fields, api
from odoo.exceptions import UserError

class BinduRegistration(models.Model):
    _name = 'bindu.registration'
    _description = 'Bindu Get Together Registration'

    name = fields.Char(string="Full Name", required=True)
    phone = fields.Char(string="Phone", required=True)
    transaction_id = fields.Char(string="Transaction ID", required=True)
    email = fields.Char(string="Email", required=True)
    partner_id = fields.Many2one('res.partner', string="Related Partner")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid'),
        ('payment_confirm', 'Payment Confirmed'),
        ('validated', 'Transaction Validated'),
    ], default='draft', string="Status", tracking=True)


    def get_report_values(self, docids, data=None):
        # Use sudo to ensure superuser access
        docs = self.sudo().browse(docids)
        return {
            'docs': docs,
            # Add any additional context or data needed for the report
        }
        
        
    def action_payment_confirm(self):
        self.state = 'payment_confirm'

    def action_transaction_validated(self):
        self.state = 'validated'

    # def action_create_invoice(self):
    #     if not self.partner_id:
    #         raise UserError('No partner found for this registration.')
        
    #     invoice = self.env['account.move'].create({
    #         'partner_id': self.partner_id.id,
    #         'move_type': 'out_invoice',
    #         'journal_id': self.env['account.journal'].search([('type', '=', 'cash')], limit=1).id,
    #         'invoice_line_ids': [(0, 0, {
    #             'name': 'Bindu Get Together Registration Fee',
    #             'quantity': 1,
    #             'price_unit': 100,  # Adjust the fee as needed
    #         })]
    #     })
    #     self.state = 'paid'
    #     return invoice

    # @api.model
    # def create(self, vals):
    #     partner = self.env['res.partner'].sudo().create({
    #         'name': vals.get('name'),
    #         'email': vals.get('email'),
    #         'phone': vals.get('phone'),
    #     })
    #     vals['partner_id'] = partner.id

    #     user_vals = {
    #         'name': vals.get('name'),
    #         'login': vals.get('email'),
    #         'partner_id': partner.id,
    #         'email': vals.get('email'),
    #         'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])]
    #     }
    #     self.env['res.users'].sudo().create(user_vals)

    #     return super(BinduRegistration, self).create(vals)