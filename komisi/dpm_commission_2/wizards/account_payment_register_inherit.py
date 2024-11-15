from odoo import models, fields, api

class AccountPaymentRegisterInherit(models.TransientModel):
    _inherit = 'account.payment.register'
    
    agent_id = fields.Many2one(
        'res.partner',
        domain=[('agent', '=', True)]
    )
    commission_id = fields.Many2one(
        'commission',
        string='Commission',
        domain=['|', 
                ('settlement_type', '=', 'sale_invoice'),
                ('settlement_type', '=', False)],
        # default=lambda self: self._get_default_commission()
    )
    
    @api.onchange('agent_id')
    def _onchange_agent_id(self):
        if self.agent_id:
            # Cari commission dari agent yang dipilih
            if self.agent_id.commission_id:
                self.commission_id = self.agent_id.commission_id
            else:
                # Jika agent tidak punya commission default, cari commission yang sesuai
                commission = self.env['commission'].search([
                    '|',
                    ('settlement_type', '=', 'sale_invoice'),
                    ('settlement_type', '=', False)
                ], limit=1)
                self.commission_id = commission.id if commission else False

    def _create_payments(self):
        payments = super()._create_payments()
        
        if self.agent_id:
            # Update agent untuk setiap invoice line
            for payment in payments:
                for move in payment.reconciled_invoice_ids:
                    for line in move.invoice_line_ids.filtered(lambda l: l.display_type == 'product'):
                        # Panggil method untuk update agent
                        line.button_edit_agents()
                        # Update agent pada line
                        self.env['account.invoice.line.agent'].create({
                            'agent_id': self.agent_id.id,
                            'object_id': line.id,
                            'commission_id': self.commission_id.id,
                        })
        return payments
        
    # def _get_default_commission(self):
    #     """Method untuk mendapatkan commission default"""
    #     commission = self.env['commission'].search([
    #         ('settlement_type', '=', 'sale_invoice'),
    #         ('invoice_state', '=', 'paid')
    #     ], limit=1)
    #     return commission.id if commission else False