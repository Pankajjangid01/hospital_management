from odoo import models, fields

class InvoiceConfirmationWizard(models.TransientModel):
    
    _name = 'invoice.confirmation.wizard'
    _description = 'Confirm Invoice Creation'

    appointment_id = fields.Many2one('appointment.appointment', string="Appointment", required=True)

    def create_invoice(self):
        """Create an invoice linked to the appointment."""
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.appointment_id.patient_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [
                (0, 0, {
                    'name': f"Appointment Invoice for {self.appointment_id.patient_id.name}",
                    'quantity': 1,
                    'price_unit': 200,
                })
            ]
        }
        invoice = self.env['account.move'].create(invoice_vals)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    @staticmethod    
    def cancel():
        """This function close the wizard window"""
        return {'type': 'ir.actions.act_window_close'}
