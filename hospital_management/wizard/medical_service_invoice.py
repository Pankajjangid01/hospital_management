from odoo import models, fields

class MedicalServiceInvoice(models.TransientModel):

    _name = 'medical.service.invoice'
    _description = 'Confirm Medical Service Invoice Creation'

    name = fields.Many2one('medical.service', string="Medical Name", required=True)

    def create_invoice(self):
        """Create an invoice linked to the medical service."""
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.name.patient_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [
                (0, 0, {
                    'name': self.name.medical_details_ids.medicine_product,
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
