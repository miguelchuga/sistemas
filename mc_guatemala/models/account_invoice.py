# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import util

class account_invoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    @api.one
    def _calcular_letras(self):
        self.numeros_a_letras =  util.num_a_letras(self.amount_total)


    serie_gt = fields.Char('Serie de la factura', size=40)
    partner_liquidacion_id = fields.Many2one('res.partner', 'Proveedor factura')
    liquidaciones_id = fields.Many2one('mc_guatemala.liquidaciones', 'Liquidacion')
    numeros_a_letras = fields.Char('Letras', compute=_calcular_letras)

class account_invoice_line(models.Model):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'

    @api.one
    def _n_total_linea(self):
        self.n_total_linea = self.quantity * self.price_unit


    n_total_linea = fields.Float('Total linea', compute=_n_total_linea)
