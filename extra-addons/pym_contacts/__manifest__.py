# -*- coding: utf-8 -*-
{
    'name': "pym_contacts",

    'summary': """
        Personalizacion Pernos y Mas, localización, factura preimpresa
        """,

    'description': """
        Personalizacion Pernos y Mas
    """,

    'author': "Kodice S.A.",
    'website': "http://www.kodice.com.ec",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['contacts',
                'l10n_ec',
                "account",
                ],
    # always loaded
    'data': [
        'data/l10n_latam_identification_type_data.xml',
        'data/res_partner_data.xml',
        'views/pym_report.xml',
        'views/account_move_view.xml',
        'views/view_out_invoice_tree.xml',
    ],
}
