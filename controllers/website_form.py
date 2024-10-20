from odoo import http
from odoo.http import request

class BinduRegistrationController(http.Controller):

    @http.route('/bindu/registration', type='http', auth='user', website=True)
    def bindu_registration_form(self, **kw):
        # Fetch the logged-in user's email
        user_email = request.env.user.email
        return request.render('bindu_registration.bindu_registration_form', {
            'user_email': user_email,  # Pass the user's email to the form
        })

    @http.route('/bindu/registration/submit', type='http', auth='user', website=True, csrf=True)
    def submit_registration(self, **post):
        partner_id = request.env.user.partner_id.id  # Get the partner_id of the logged-in user
        vals = {
            'name': post.get('name'),
            'phone': post.get('phone'),
            'transaction_id': post.get('transaction_id'),
            'email': post.get('email'),
            'partner_id': partner_id  # Set the partner_id to the logged-in user
        }
        # Use sudo to bypass access restrictions for normal users
        registration = request.env['bindu.registration'].sudo().create(vals)
        return request.render('bindu_registration.thank_you', {'registration': registration})

    @http.route('/my/registrations', type='http', auth='user', website=True)
    def web_bindu_registrations(self):
        # Fetch the registrations related to the logged-in user
        registrations = request.env['bindu.registration'].sudo().search([('partner_id', '=', request.env.user.partner_id.id)])
        return request.render('bindu_registration.web_bindu_registration', {
            'registrations': registrations,
        })
        
class BinduRegistrationController(http.Controller):

        @http.route('/download/ticket/<int:registration_id>', type='http', auth='public', website=True)
        def download_ticket(self, registration_id, **kwargs):
            # Retrieve the registration record
            registration = request.env['bindu.registration'].sudo().browse(registration_id)
            if not registration.exists():
                return request.not_found()

            # Generate the PDF report
            report_action = request.env['ir.actions.report'].sudo()._get_report_from_name('bindu_registration.action_report_bindu_registration')
            
            # Check if the report exists
            if not report_action:
                return request.not_found()

            # Render the PDF
            pdf_data = report_action._render_qweb_pdf([registration.id])[0]

            # Prepare the response
            response = request.make_response(pdf_data,
                headers=[
                    ('Content-Type', 'application/pdf'),
                    ('Content-Disposition', 'attachment; filename="ticket_{}.pdf"'.format(registration_id))
                ]
            )
            return response