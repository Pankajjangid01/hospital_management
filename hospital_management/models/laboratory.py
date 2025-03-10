from odoo import models,fields,api

class DraftLaboratory(models.Model):

    _name = "draft.laboratory"
    _description = "This model store the lab test that to be done"
    _rec_name = "test_type_name"

    request_id = fields.Char(default=lambda self: ('New'), readonly=True)
    test_type_name = fields.Many2one("test.type",string="Test Type",required=True)
    test_date = fields.Datetime(string="Date")
    invoice_to_insaurance = fields.Boolean(string="Invoice to Insaurance")
    patient_id = fields.Many2one("patient.patient",string="Patient",required=True)
    patient_doctor = fields.Char(string="Doctor", readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('tested', 'Tested'),
        ('cancel', 'Cancelled')
    ], string="Status", default='draft', tracking=True)

    @api.onchange("patient_id")
    def _onchange_patient_id(self):
        for record in self:
            if record.patient_id:
                record.patient_doctor = record.patient_id.patient_primary_care_doctor_id.physisican_name.name
            else:
                record.patient_doctor = ""

    def create(self, vals):
        """Automatically generate a Lab test request sequence."""
        vals['request_id'] = self.env['ir.sequence'].next_by_code('draft.laboratory')
        return super(DraftLaboratory, self).create(vals)

    def action_open_test_wizard(self):
        """Function to open the Lab test wizard"""
        return {
            'name': ('Create Lab Result'),
            'type': 'ir.actions.act_window',
            'res_model': 'lab.result',
            'view_mode': 'form',
            'view_id': self.env.ref('hospital_management.lab_result_wizard_form').id,
            'target': 'new',
            'context': {'default_laboratory_id': self.id} 
        }

    def action_cancel(self):
        """Mark test as Cancelled"""
        self.state = 'cancel'

    def action_open_lab_test_invoice_wizard(self):
        """this method opens the lab test confirmation invoice wizard"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Lab Test Invoice Confirmation',
            'res_model': 'lab.test.invoice.confirmation.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_test_type': self.id},
        }
