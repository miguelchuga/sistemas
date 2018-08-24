#!/usr/bin/python
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class account_account(models.Model):

    _name = 'account.account'
    _inherit = 'account.account'

    compras_locales = fields.Boolean('Compras locales')
    compras_importaciones = fields.Boolean('Compras Importaciones')
    impuesto_iva = fields.Boolean('Iva compras')
    impuesto_exentos = fields.Boolean('impuestos exentos')


    ventas_locales = fields.Boolean('Ventas locales')
    ventas_impuesto_iva = fields.Boolean('Iva Ventas')
    ventas_impuesto_exentos = fields.Boolean('impuestos exentos ventas')
    ventas_exportacion = fields.Boolean('Ventas Exportación')
    ventas_base_imponible = fields.Boolean('Venta base imponible')
