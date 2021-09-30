odoo.define('pym_config.PaymentScreen', function(require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    var { Gui } = require('point_of_sale.Gui');
    var models = require('point_of_sale.models');
    var rpc = require('web.rpc');


    const PosPaymentScreen = PaymentScreen =>
        class extends PaymentScreen {

            async _finalizeValidation() {
                await super._finalizeValidation();
                console.log('PaymentScreen _finalizeValidation');
                var pym_physical_invoice_number = $('input.physical_invoice_number').val();
                if (pym_physical_invoice_number && !isNaN(pym_physical_invoice_number)) {
                    this.currentOrder.set_physical_invoice_number(pym_physical_invoice_number.trim());
                }
                var order = this.currentOrder;
                if (order.is_to_invoice() && order.get_physical_invoice_number() != '') {
                    rpc.query({
                        model: 'pos.order',
                        method: 'search_read',
                        domain: [['pos_reference', '=', order['name']]],
                        fields: ['account_move'],
                    }).then(function (orders) {
                        if (orders.length > 0) {
                            if (orders[0]['account_move']) {
                                order.invoice_number = orders[0]['account_move'][1].split(" ")[0];
                                console.debug("ORDER invoice name: %s", order.invoice_number);

                                rpc.query({
                                    model: 'account.move',
                                    method: 'search_read',
                                    domain: [['name', '=', order.invoice_number]],
                                    fields: ['id'],
                                }).then(function (invoices) {
                                    if (invoices.length > 0) {
                                        if (invoices[0]['id']) {
                                            order.invoice_id = invoices[0]['id'];
                                            console.debug("Invoice ID: %s --> %s", order.invoice_id, order.physical_invoice_number);
                                            rpc.query({
                                                model: 'account.move',
                                                method: 'write',
                                                args: [order.invoice_id, {physical_invoice_number: order.physical_invoice_number}],
                                            }).then(function (invoices) {
                                                console.debug("Actualizando Invoice ID: %s con: %s", order.invoice_id, order.physical_invoice_number);
                                            });
                                        }
                                    }
                                });
                            }
                        }
                    });
                }

            }
        };

    Registries.Component.extend(PaymentScreen, PosPaymentScreen);

    return PaymentScreen;
});
