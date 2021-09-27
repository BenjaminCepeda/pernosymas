odoo.define('pym_config.models', function (require) {
    "use strict";

    var models = require('point_of_sale.models');

    models.load_fields('account.move', ['physical_invoice_number',]);
    models.load_fields('res.partner', [
                                          'l10n_latam_identification_type_id']);

    models.load_models([
        {
            model: 'l10n_latam.identification.type',
            fields: [],
            loaded: function (self, identification_type) {
                self.identification_type = identification_type;
            }
        }
    ]);


});
