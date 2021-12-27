from .models import Product

class SessionProduct:
    '''object of this class will be in session'''
    id = 0
    name = ''
    image = ''
    sales_price = 0.0
    quantity = 0

    def get_session_product(self,product_id,product_quantity):
        session_product = SessionProduct()
        productdetail = Product.objects.get(id=product_id)
        session_product.id = product_id
        session_product.quantity += int(product_quantity)
        session_product.name = productdetail.name
        session_product.image = productdetail.image
        session_product.sales_price = productdetail.sale_price
        return session_product


