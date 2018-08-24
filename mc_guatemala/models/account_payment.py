# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import util

class account_payment(models.Model):
    _name = 'account.payment'
    _inherit = 'account.payment'

    
    @api.one
    def _calcular_letras(self):
        self.numeros_a_letras =  util.num_a_letras(self.amount)


    liquidaciones_id = fields.Many2one('mc_guatemala.liquidaciones', 'Liquidacion')
    numeros_a_letras = fields.Char('Letras', compute=_calcular_letras)

    @api.one
    @api.depends('invoice_ids', 'payment_type', 'partner_type', 'partner_id')
    def _compute_destination_account_id(self):
        if self.invoice_ids:
            self.destination_account_id = self.invoice_ids[0].account_id.id
        elif self.payment_type == 'transfer':
            if not self.company_id.transfer_account_id.id:
                raise UserError(_('Transfer account not defined on the company.'))
            self.destination_account_id = self.company_id.transfer_account_id.id
        elif self.partner_id:
            if self.partner_type == 'customer':
                self.destination_account_id = self.partner_id.property_account_receivable_id.id
            else:
                if self.x_account_id:
                    self.destination_account_id = self.x_account_id.id
                    print self.destination_account_id 
                else:
                    self.destination_account_id = self.partner_id.property_account_payable_id.id


    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if not self.x_account_id and self.payment_type == 'outbound':
            self.x_account_id = self.partner_id.property_account_payable_id.id


    @api.multi
    def unlink(self):
        if any(bool(rec.move_line_ids) for rec in self):
            raise UserError(_("You can not delete a payment that is already posted"))
        if self.ids:
            for i in self.ids:
                _payment_id = self.env['account.payment'].browse(i)
                if _payment_id.state == 'draft':
                    _payment_id.write({'move_name':""}) 
                    print _payment_id.move_name

        return super(account_payment, self).unlink()


    x_recibo_caja = fields.Char('Recibo de caja')
    x_deposito = fields.Char('No. deposito')
    numeros_a_letras = fields.Char('Letras', compute=_calcular_letras)
    x_no_negociable = fields.Boolean('NO NEGOCIABLE : ', default=True )
    x_account_id = fields.Many2one('account.account', string='Cuenta')

    
    