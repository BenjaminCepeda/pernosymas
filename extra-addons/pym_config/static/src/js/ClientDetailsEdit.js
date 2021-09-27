odoo.define('pym_config.ClientDetailsEdit', function (require) {
    'use strict';

    const ClientDetailsEdit = require('point_of_sale.ClientDetailsEdit');
    const Registries = require('point_of_sale.Registries');
    var {Gui} = require('point_of_sale.Gui');
    var models = require('point_of_sale.models');

    const POSSaveClientOverride = ClientDetailsEdit =>
        class extends ClientDetailsEdit {

            async saveChanges(event) {

                try {

                    var jm_name = $('input.client-name').val();
                    var jm_l10n_latam_identification_type_id = $('.l10n_latam_identification_type_id').val();
                    var jm_identification_number = $('.vat').val();
                    var jm_identification_type = $('.l10n_latam_identification_type_id').find('option:selected').text();
                    var ruc_vat_type = jm_identification_type.trim().toUpperCase() =='RUC';
                    var ced_vat_type = (jm_identification_type.trim().toUpperCase() == 'CEDULA' ||
                        jm_identification_type.trim().toUpperCase() =='CÉDULA');

                    if (!jm_name || jm_name.trim() == '') {

                        await this.showPopup('ErrorPopup', {
                            title: this.env._t(jm_identification_type),
                            body: this.env._t('Debe completar el campo Nombre'),
                        });
                        return;
                    } else if (jm_l10n_latam_identification_type_id == '0') {

                        await this.showPopup('ErrorPopup', {
                            title: this.env._t('Tipo Id. debe completarse'),
                            body: this.env._t('Debe completar el campo Tipo Identificación'),
                        });
                        return;
                    } else if (!jm_identification_number || jm_identification_number.trim() == '') {

                        await this.showPopup('ErrorPopup', {
                            title: this.env._t('Número de Identificación debe completarse'),
                            body: this.env._t('Debe completarse el campo Número de Identificación'),
                        });
                        return;
                    } else if (ruc_vat_type || ced_vat_type){
                        var l= jm_identification_number.length;
                        if (isNaN(jm_identification_number)) {
                            await this.showPopup('OfflineErrorPopup', {
                                title: this.env._t('Número de Identificación incorrecta'),
                                body: this.env._t('Número de Identificación debe ser numérica'),
                            });
                            return;
                        } else if (!((l == 10 && ced_vat_type)
                            || (l == 13 && ruc_vat_type))) {
                            await this.showPopup('OfflineErrorPopup', {
                                title: this.env._t('Número de Identificación incorrecta'),
                                body: this.env._t('Número de dígitos no corresponde al Tipo de Id.'),
                            });
                            return;
                        }
                    }
                    let processedChanges = {};
                    for (let [key, value] of Object.entries(this.changes)) {
                        if (this.intFields.includes(key) || key=='l10n_latam_identification_type_id') {
                            processedChanges[key] = parseInt(value) || false;
                        } else {
                            processedChanges[key] = value;
                        }
                    }
                    processedChanges.id = this.props.partner.id || false;
                    this.trigger('save-changes', { processedChanges });
                } catch (error) {
                    if (error.message.code < 0) {
                        await this.showPopup('OfflineErrorPopup', {
                            title: this.env._t('Offline'),
                            body: this.env._t('Unable to save changes.'),
                        });
                    } else {
                        throw error;
                    }
                }
            }
        };

    Registries.Component.extend(ClientDetailsEdit, POSSaveClientOverride);

    return ClientDetailsEdit;

});
