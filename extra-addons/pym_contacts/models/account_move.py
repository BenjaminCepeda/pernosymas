from odoo import fields, models, _

class ResPartner(models.Model):
    _inherit = 'account.move'
    physical_invoice_number = fields.Integer(string="Número de factura física",required="False")