from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    _description = 'Adding Last Price'
    
    last_price = fields.Float(
        string="Last Price",
        default = 0.0,
        compute='_compute_last_price',
        readonly=True)
    
    
    def get_last_price(self, product_id):
        record = self.search([('product_id.id', '=', product_id.id), ('order_id.state', 'in', ['done'])], order ='create_date desc', limit=1)
        if record:
            return record.price_unit
        return 0
        
        
    @api.depends('product_id', 'order_id.state')
    def _compute_last_price(self):
        for record in self:
            print("order id state", record.order_id.state)
            if record.product_id:
                lp = self.get_last_price(record.product_id)
                print("last price is", lp)
                record.last_price = self.get_last_price(record.product_id)
            else:
                record.last_price = 0
                
