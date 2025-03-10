from odoo import models,fields,api

class LabTestInfo(models.Model):

    _name = "lab.test.info"
    _description = "This model store the created test result"
    _rec_name = "test_id"

    test_id = fields.Char(readonly=True,string="Id")
    date_of_analysis = fields.Datetime(string="Date of Analysis")
    pathologist_physician = fields.Char(string="Pathologist Physician", readonly = True)
    test_type = fields.Char(string="Test Type",readonly=True)
    patient_id = fields.Many2one('patient.patient',string="Patient")
    date_requestes = fields.Datetime(string="Date requested")
    total_cases_ids = fields.Many2many('patient.total.cases')
    results = fields.Char(string="Results")
    diagnosis = fields.Boolean(string="Diagnosis")
    
    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        """Get the test type of the seleceted patient"""
        for record in self:
            if record.patient_id:
                patient_test_type = self.env['draft.laboratory'].search([('patient_id','=',self.patient_id.id)])
                record.test_type = patient_test_type.test_type_name.name
                record.test_id = patient_test_type.test_type_name.test_code
                record.pathologist_physician = patient_test_type.patient_doctor
            else:
                record.pathologist_physician = ""

class PatientTotalCases(models.Model):

    _name = "patient.total.cases"
    _description = "This model stores the total cases of patient"

    sequence = fields.Char(default=lambda self: ('New'),readonly=True, copy=False,string="sequence")
    case_name = fields.Char(string="Name")
    case_result = fields.Char(string="Result Text")
    normal_range = fields.Char(string="Normal Range")
    units = fields.Integer(string="Units")

    @api.model
    def create(self, vals):
        """Automatically generate a sequence number for new test case."""
        vals['test_id'] = self.env['ir.sequence'].next_by_code('patient.total.cases')
        return super(PatientTotalCases, self).create(vals)
