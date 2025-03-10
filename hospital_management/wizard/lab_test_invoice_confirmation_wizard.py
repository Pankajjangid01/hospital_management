from odoo import models, fields

class LabTestInvoiceConfirmationWizard(models.TransientModel):
    
    _name = 'lab.test.invoice.confirmation.wizard'
    _description = 'Confirm Lab test Invoice Creation'

    test_type = fields.Many2one('draft.laboratory"', string="Lab Test", required=True)

    def create_invoice(self):
        """Create an invoice linked to the laboratory."""
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.test_type.patient_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [
                (0, 0, {
                    'name': f"{self.test_type}",
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
