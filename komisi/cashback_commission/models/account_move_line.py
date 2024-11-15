from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    cashback_percentage = fields.Float(string='Cashback %', digits=(5,2))
    cashback_amount = fields.Monetary(string='Cashback Amount', compute='_compute_cashback_values', store=True)
    price_after_cashback = fields.Monetary(string='Price After Cashback', compute='_compute_cashback_values', store=True)

    @api.depends('price_subtotal', 'cashback_percentage')
    def _compute_cashback_values(self):
        for line in self:
            # Hitung cashback_amount
            if line.price_subtotal and line.cashback_percentage:
                # Rumus: cashback_amount = price_subtotal * (cashback_percentage/100)
                line.cashback_amount = (line.price_subtotal * line.cashback_percentage) / 100
            else:
                line.cashback_amount = 0.0

            # Hitung price_after_cashback
            # Rumus: price_after_cashback = price_subtotal - cashback_amount
            line.price_after_cashback = line.price_subtotal - line.cashback_amount

    def write(self, vals):
        res = super().write(vals)
        if 'cashback_percentage' in vals:
            self._compute_cashback_values()
        return res