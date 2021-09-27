# -*- coding: utf-8 -*-


from . import models
from odoo import api, SUPERUSER_ID

def _set_default_identification_type(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    if env:
        env['res.partner'].search([]).\
        write({'l10n_latam_identification_type_id': env.\
        ref('pym_config.ec_ruc').id})