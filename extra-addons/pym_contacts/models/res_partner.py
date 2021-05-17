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

    @api.onchange('country_id')
    def _onchange_country(self):
        country = self.country_id or self.company_id.country_id or self.env.company.country_id
        ec_code = self.env['res.country'].search([('code', '=', 'EC')],
                                                 limit=1)
        if country == ec_code:
            self.l10n_latam_identification_type_id =\
                self.env.ref('pym_contacts.ec_ruc')

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
                        _('invalid ID length '))
            if self.l10n_latam_identification_type_id == ced_vat_type:
                mod9=pym_util.PymUtil.verificar(vat)
                if not mod9:
                    raise ValidationError(_('invalid ID number '))
            elif self.l10n_latam_identification_type_id == ruc_vat_type and \
                    vat != '9999999999999':
                mod9= pym_util.PymUtil.verificar(vat)
                if not mod9:
                    raise ValidationError(_('invalid ID number '))
        return True

    def _get_direccion(self):
        self.direccion = self.street + ' ' + self.street2

    country_id = fields.Many2one('res.country', string='Country',
                                 default=_get_default_country)
    direccion=fields.Char(compute=_get_direccion, string='Dirección completa')