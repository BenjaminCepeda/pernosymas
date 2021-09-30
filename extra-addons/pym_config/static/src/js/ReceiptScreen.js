odoo.define('pym_config.ReceiptScreen', function (require) {
    'use strict';

    var models = require('point_of_sale.models');
    var ReceiptScreen = require('point_of_sale.ReceiptScreen');
    const Registries = require('point_of_sale.Registries');
    var { Gui } = require('point_of_sale.Gui');
    var rpc = require('web.rpc');

    const pym_Receipt_Screen = ReceiptScreen => {
        class pym_Receipt_Screen extends ReceiptScreen {
            constructor() {
                super(...arguments);
                console.debug("ReceiptScreen function");
                var self = this;

                if (this.pos.config.receipt_invoice_number) {
                    self.receipt_data = this.get_receipt_render_env();
                    var order = this.pos.get_order();
                    return rpc.query({
                        model: 'pos.order',
                        method: 'search_read',
                        domain: [['pos_reference', '=', order['name']]],
                        fields: ['invoice_id'],
                    }).then(function (orders) {
                        if (orders.length > 0) {
                            if (orders[0]['invoice_id']) {
                                var invoice_number = orders[0]['invoice_id'][1].split(" ")[0];
                                self.receipt_data['order']['invoice_number'] = invoice_number;
                                console.debug(invoice_number);
                            }
                        }
                    });
                }
            }
        }
        return pym_Receipt_Screen;
    }
    Registries.Component.extend(ReceiptScreen, pym_Receipt_Screen);

    return ReceiptScreen;


});
