from odoo import models, fields

class AppointmentEvaluation(models.TransientModel):
    _name = "appointment.evaluation"
    _description = "This model stores the appointment evaluation data per doctor"

    name_of_physician = fields.Many2many('appointment.appointment', string="Name of Physician")
    speciality = fields.Char(string="Speciality")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    def show(self):
        """Filters appointments based on the provided field values and opens the filtered list"""
        domain = []

        if self.name_of_physician:
            domain.append(('physician', 'in', self.name_of_physician.mapped('physician')))

        if self.speciality:
            domain.append(('speciality', '=', self.speciality))

        if self.start_date:
            domain.append(('appointment_date', '>=', self.start_date))

        if self.end_date:
            domain.append(('appointment_end', '<=', self.end_date))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Filtered Appointments',
            'res_model': 'appointment.appointment',
            'view_mode': 'list,form',
            'domain': domain,
            'target': 'current',
        }
    
    @staticmethod
    def cancel():
        """Closes the wizard window"""
        return {'type': 'ir.actions.act_window_close'}
