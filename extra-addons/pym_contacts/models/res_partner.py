# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from . import pym_util


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _get_default_country(self):
        country = self.env['res.country'].search([('code', '=', 'EC')],
                                                 limit=1)
        return country

    country_id = fields.Many2one('res.country', string='Country',
                                 default=_get_default_country)
    # @api.model
    # def _get_default_l10n_latam_identification_type_id(self):
    #     ruc_vat_type = self.env.ref('pym_contacts.ec_ruc')
    #     return ruc_vat_type
    #
    # l10n_latam_identification_type_id =\
    #     _get_default_l10n_latam_identification_type_id

    def check_vat_ec(self, vat):
        l = len(vat)
        if self.l10n_latam_identification_type_id.is_vat:
            ruc_vat_type = self.env.ref('pym_contacts.ec_ruc')
            ced_vat_type = self.env.ref('pym_contacts.ec_dni')
            if self.l10n_latam_identification_type_id in (ruc_vat_type, ced_vat_type):
                # temporal fix as stdnum.ec is allowing old format with a dash in between the number
                if not self.vat.isnumeric():
                    #raise ValidationError(_('Ecuadorian VAT number must contain only numeric characters'))
                    raise ValidationError(_("Id must only contain numbers"))
                if not ((l == 10 and
                         self.l10n_latam_identification_type_id == ced_vat_type)
                        or (l == 13 and
                            self.l10n_latam_identification_type_id == ruc_vat_type)):
                    #raise ValidationError(_('Invalid  VAT number must contain only numeric characters'))
                    raise ValidationError(
                        _('invalid ID number '))
            if self.l10n_latam_identification_type_id == ced_vat_type:
                return pym_util.PymUtil.verificar(vat)
            elif self.l10n_latam_identification_type_id == ruc_vat_type and \
                    vat != '9999999999999':
                return pym_util.PymUtil.verificar(vat)
        return True
