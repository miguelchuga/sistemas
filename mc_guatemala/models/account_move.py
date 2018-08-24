# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import util

class account_move(models.Model):
    _name = 'account.move'
    _inherit = 'account.move'


    liquidaciones_id = fields.Many2one('mc_guatemala.liquidaciones', 'Liquidacion')
