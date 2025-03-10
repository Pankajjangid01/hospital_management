from odoo import models, fields

class PrescriptionInvoiceConfirmationWizard(models.TransientModel):
    
    _name = 'prescription.invoice.confirmation.wizard'
    _description = 'Confirm Prescription Invoice Creation'

    prescription_id = fields.Many2one('prescription.prescription', string="prescription", required=True)

    def create_invoice(self):
        """Create an invoice linked to the prescription."""
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.prescription_id.patient_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [
                (0, 0, {
                    'name': f"Prescription Invoice for {self.prescription_id.patient_id.name}",
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
