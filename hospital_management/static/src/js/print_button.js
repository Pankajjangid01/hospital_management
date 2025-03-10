import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { onMounted } from "@odoo/owl";

patch(FormController.prototype, {
    setup() {
        super.setup();
        var self = this
        onMounted(() => {
            if (self.props.resModel == 'patient.patient') {
                const addButton = document.querySelector('.btn btn-secondary o-dropdown dropdown-toggle dropdown button[aria-expanded="false"]');
                if (addButton) {
                    addButton.style.display = 'none';
                }
            }
        });
},
})