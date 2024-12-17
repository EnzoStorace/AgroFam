from django.contrib import admin
from .models import MenuItem, Category, OrderModel, Seller
from django.contrib.auth.models import User

admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)
admin.site.register(Seller)