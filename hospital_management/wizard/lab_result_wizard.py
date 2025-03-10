from odoo import models,fields

class LabResult(models.TransientModel):
    
    _name = "lab.result"
    _description = "Create the lab test result"

    laboratory_id = fields.Many2one("draft.laboratory", string="Lab Test")

    def confirm(self):
        """Confirm test and mark as Tested"""
        if self.laboratory_id:
            self.laboratory_id.state = 'tested'

        return {
            'name': 'Lab Test Result Info',
            'type': 'ir.actions.act_window',
            'res_model': 'lab.test.info',
            'view_mode': 'list,form',
        }

    @staticmethod    
    def cancel():
        """This function close the wizard window"""
        return {'type': 'ir.actions.act_window_close'}
