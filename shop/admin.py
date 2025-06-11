from django.contrib import admin
from .models import Brand, Product,Cart,CartItem,Sale,SaleItem

admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Sale)
admin.site.register(SaleItem)
