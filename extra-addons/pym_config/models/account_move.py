from odoo import fields, models, _

class AccountMove(models.Model):
    _inherit = 'account.move'
    physical_invoice_number = fields.Integer(string="Fac.física",
                                             required="False",default=0)
    invoice_partner_vat = fields.Char(string='Identificación',
                                      related='partner_id.vat')