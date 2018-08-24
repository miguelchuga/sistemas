# -*- coding: utf-8 -*-

{
    'name': 'Extra para localizacion Guatemala - MC-Sistemas',
    'version': '2.0.0',
    'author': 'MC-Sistemas',
    'summary': 'Datos extras para la localizacion de Guatemala ',
    'description' : """
========================
- Odoo para Guatemala
========================
    """,
    'website': 'http://mcsistemas.net',
    'category': 'Accounting & Finance',
    'depends': ["account",
                "account_check_printing"],
    'data': [
        'views/account_account_view.xml',
        'views/account_journal_view.xml',
        'views/account_invoice_view.xml',
        'views/account_payment_view.xml',
        'views/account_move_view.xml',
        'views/liquidaciones_view.xml',

#        'views/generate_libro_ventas_wizard.xm    l',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}