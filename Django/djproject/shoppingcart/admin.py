from django.contrib import admin
# Register your models here.

from .models import Cateogary


from .models import SaleOrderItem
from .models import SalesOrder
from .models import Product
from .models import User
from .models import Address
from .models import Profile

admin.site.register(Product)
admin.site.register(SaleOrderItem)
admin.site.register(SalesOrder)
admin.site.register(Cateogary)
admin.site.register(User)
admin.site.register(Address)
admin.site.register(Profile)



