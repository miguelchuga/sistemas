# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.tools.sql import drop_view_if_exists


STATE_SELECTION = [
    ('draft', 'Draft'),
    ('aceptada', 'Aceptada'),
    ('liquidada', 'Liquidada')
]


class liquidaciones(models.Model):
    _name = 'mc_guatemala.liquidaciones'
    _description = 'Liquidaciones de gastos'
    _inherit = 'mail.thread'


    
    name = fields.Char("Descripción")
    date = fields.Datetime(string='Fecha', default=fields.Datetime.now)
    partner_id = fields.Many2one('res.partner', 'Responsable')
    facturas_ids = fields.One2many('account.invoice', 'liquidaciones_id', string='Facturas')
    cheques_ids = fields.One2many('account.payment', 'liquidaciones_id', string='Cheques')
    move_ids = fields.One2many('account.move', 'liquidaciones_id', string='Asiento contable')

    liquidacion_ids = fields.One2many('mc_guatemala.liquidaciones.detalle', 'liquidaciones_id', string='Liquidacion detalle', copy=True)

    state = fields.Selection(STATE_SELECTION, 'Status', default='draft')

    @api.one
    @api.depends('cheques_ids','facturas_ids')
    def _ipo(self):
        t=timedelta(days=self.duration-1)
        start=self.start_date.split('-')       
        self.end_date=date(int(start[0]),int(start[1]),int(start[2]))+t

    @api.one
    def aceptada(self):
        self.state = 'aceptada'

    @api.one
    def liquidada(self):
        self.state = 'liquidada'

    @api.one
    def anulada(self):
        self.state = 'anulada'

    @api.multi
    def concilia_apuntes(self):
        journal_entries_id = []
        #Facturas
        if self.facturas_ids._ids:
            for i in self.facturas_ids:
                invoice_line_ids = self.env['account.invoice'].browse([i.id]).move_id.line_ids.ids
                if invoice_line_ids:
                    for l in invoice_line_ids:
                        move_line_id = self.env['account.move.line'].browse(l)
                        if move_line_id.account_id.internal_type == "payable" and move_line_id.account_id.reconcile == True:
                            journal_entries_id.append(l)
        print journal_entries_id
        #Cheques
        if self.cheques_ids._ids:
            for i in self.cheques_ids:
                check_line_ids = self.env['account.payment'].browse(i.id).move_line_ids
                if check_line_ids:
                    for l in check_line_ids:
                        if l.account_id.internal_type == "payable" and l.account_id.reconcile == True:
                            journal_entries_id.append(l.id)
        print journal_entries_id
        #Asientos contables
        if self.move_ids:
            for m in self.move_ids:
                for l in m.line_ids:
                    if l.account_id.internal_type == "payable" and l.account_id.reconcile == True:
                            journal_entries_id.append(l.id)

        print journal_entries_id
        if journal_entries_id:
            return {"type": "ir.actions.act_window",
             "res_model": "account.move.line",
             'view_type': 'form',
             'view_mode': 'tree',
             "target": "current",
             'domain': [('id', 'in', journal_entries_id)]
            }
        print "mm"


class liquidaciones_detalle(models.Model):
    _name = 'mc_guatemala.liquidaciones.detalle'
    _description = 'Liquidacion detalle'
    _order = 'liquidaciones_id, tipo'


    liquidaciones_id = fields.Many2one('mc_guatemala.liquidaciones', 'Liquidacion')
    invoice_id = fields.Many2one('account.invoice', 'Factura')
    payment_id = fields.Many2one('account.payment', 'Cheque')
    tipo = fields.Char("Tipo")
    
    