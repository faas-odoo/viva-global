from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _description = 'Adding Last Price'
    
    last_price = fields.Float(
        string="Last Price",
        default = 0.0,
        compute='_compute_last_price',
        readonly=True)
    
    
    def get_last_price(self, product_id, partner_id):
        record = self.search([('product_id.id', '=', product_id.id), ('order_id.partner_id', '=', partner_id.id), ('order_id.state', 'in', ['sale', 'done'])], order ='create_date desc', limit=1)
        print("record is:", record)
        if record:
            return record.price_unit
        return 0
        
        
    @api.depends('product_id', 'order_partner_id')
    def _compute_last_price(self):
        for record in self:
            if record.order_partner_id and record.product_id:
                record.last_price = self.get_last_price(record.product_id, record.order_partner_id)
        
            else:
                record.last_price = 0