from odoo import fields, models, _

class ResPartner(models.Model):
    _inherit = 'account.move'
    physical_invoice_number = fields.Integer(string="Fac.física",required="False")
    invoice_partner_vat = fields.Char(string='Identificación', related='partner_id.vat')