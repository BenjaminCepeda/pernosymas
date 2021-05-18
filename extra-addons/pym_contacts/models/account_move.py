from odoo import fields, models, _

class ResPartner(models.Model):
    _inherit = 'account.move'
    physical_invoice_number = fields.Integer(string="factura física",required="False")
    invoice_partner_vat = fields.Char(string='vat', related='partner_id.vat')