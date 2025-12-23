from django.db import models
from decimal import Decimal

class CartModel(models.Model):
    user = models.ForeignKey("accounts.User",on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
  
    def calculate_total_price(self):
     total = sum(
        (item.product.get_price() * item.quantity)
        for item in self.cart_items.all()
    )
     return total if total is not None else Decimal('0')


class CartItemModel(models.Model):
    cart = models.ForeignKey(CartModel,on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey("shop.ProductModel", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title} {self.cart.user}"
    
   