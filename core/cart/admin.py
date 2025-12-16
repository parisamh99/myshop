from django.contrib import admin

from cart.models import CartModel,CartItemModel

@admin.register(CartModel)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ("id","user")

@admin.register(CartItemModel)
class CartItemModelAdmin(admin.ModelAdmin):
    list_display = ("cart","product","quantity")

