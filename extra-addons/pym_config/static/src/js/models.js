odoo.define('pym_config.models', function (require) {
    "use strict";

    var models = require('point_of_sale.models');


    models.load_fields('pos.config', [ 'pos_auto_invoice', 'receipt_invoice_number',
                                          'receipt_customer_vat']);
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


    var _super_order = models.Order.prototype;
    var physical_invoice_number ='';
    var _super_Order = models.Order.prototype;

    models.Order = models.Order.extend({
        set_physical_invoice_number: function (physical_invoice_number) {
            this.physical_invoice_number = physical_invoice_number;
        },
        get_physical_invoice_number: function () {
            return this.physical_invoice_number;
        },
        initialize: function (attributes, options) {
            _super_Order.initialize.apply(this, arguments);
            if (this.pos.config.pos_auto_invoice) {
                this.to_invoice = true;
            }
        },
        init_from_JSON: function (json) {
            var res = _super_Order.init_from_JSON.apply(this, arguments);
            if (json.to_invoice) {
                this.to_invoice = json.to_invoice;
            }
        }
    });

    var _super_PosModel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var partner_model = _.find(this.models, function (model) {
                return model.model === 'res.partner';
            });
            partner_model.fields.push('vat');
            _super_PosModel.initialize.apply(this, arguments);
        }
    });
});
