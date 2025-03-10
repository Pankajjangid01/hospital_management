from odoo import models, fields,exceptions
from odoo.exceptions import ValidationError

class HospitalBedTransferWizard(models.TransientModel):
    """Class to show the wizard for bed transfer"""
    
    _name = "hospital.bed.transfer.wizard"
    _description = "Hospital Bed Transfer Wizard"

    administration_id = fields.Many2one('administration.administration', string="Patient")
    from_bed = fields.Many2one('hospital.bed', string="Current Bed", required=True, readonly=True)
    to_bed = fields.Many2one(
        'hospital.bed',
        string="New Bed", 
        required=True,
        domain=[('is_allocated', '=', False)]
    )
    reason = fields.Text(string="Reason", required=True)

    def action_transfer_bed(self):
        """Method to transfer the patient bed"""
        if self.to_bed == self.from_bed:
            raise ValidationError("Cannot tranfer on the same bed. Please select valid bed number")

        if self.to_bed.is_allocated:
            raise exceptions.ValidationError("Selected bed is already occupied.")

        self.env['bed.transfer'].create({
            'administration_id': self.administration_id.id,
            'from_bed': self.from_bed.id,
            'to_bed': self.to_bed.id,
            'reason': self.reason,
        })

        self.from_bed.is_allocated = False
        self.to_bed.is_allocated = True

        if self.from_bed.health_center_bed_id:
            self.from_bed.health_center_bed_id.status = 'free'
        if self.to_bed.health_center_bed_id:
            self.to_bed.health_center_bed_id.status = 'occupied'

        self.administration_id.hospital_bed_num = self.to_bed.id
