from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        for order in self:
            # Cek setiap order line
            for line in order.order_line.filtered(lambda l: l.product_id and not l.commission_free):
                if not line.agent_ids:
                    raise ValidationError(_(
                        'Please set commission first before confirm the quotation.\n'
                        'You can set it by clicking the "Edit Salesperson" button (users icon).'
                    ))
        return super().action_confirm()