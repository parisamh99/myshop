from django.db import models
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator

class OrderStatusType(models.IntegerChoices):
    pending = 1
    processing = 2
    shipped = 3
    delivered = 4
    canceled = 5

class CouponModel(models.Model):
    code = models.CharField(max_length=100)
    discount_percent = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100)])
    limited_usage = models.PositiveIntegerField(default=10)
    used_by = models.ManyToManyField("accounts.User", related_name="coupon_user",blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)  
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code
    

class UserAddressModel(models.Model):
    user = models.ForeignKey("accounts.User",on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)



class OrderModel(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.PROTECT)

    #Address model for order
    address = models.CharField(max_length=250)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.IntegerField()
    payment = models.ForeignKey('payment.Payment',on_delete=models.SET_NULL,null=True,blank=True)
    total_price = models.DecimalField(max_digits=10,default=0,decimal_places=2)
    status = models.IntegerField(choices=OrderStatusType.choices,default=OrderStatusType.pending.value)
    coupon = models.ForeignKey(CouponModel, on_delete=models.PROTECT, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    
    def calculate_total_price(self):
     total = sum(
        (item.price * item.quantity)
        for item in self.order_item.all()
    )
     return total if total is not None else Decimal('0')
    
    def get_price(self):
     if self.coupon:
        discount = (self.total_price * Decimal(self.coupon.discount_percent)) / Decimal('100')
        return self.total_price - discount
     return self.total_price
    
    def get_status(self):
       return {
          "id": self.status,
          "title": OrderStatusType(self.status).name,
          "lable":OrderStatusType(self.status).label
       }
    

    def get_full_address(self):
       return f"{self.state},{self.city},{self.address}"



class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel,on_delete=models.CASCADE, related_name="order_item")
    product = models.ForeignKey("shop.ProductModel", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0,max_digits=10,decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.order) 
