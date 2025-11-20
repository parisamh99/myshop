from django.db import models
from decimal import Decimal

class StatusProductType(models.IntegerChoices):
    publish = 1 ,("نمایش")
    draft = 2 ,("عدم نمایش")



class ProductCategoryModel(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class ProductModel(models.Model):
    user = models.ForeignKey('accounts.User',on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True, unique=True)
    image = models.ImageField(default="/default/product-image.png", upload_to='product/img/')
    proudct_category = models.ManyToManyField(ProductCategoryModel)
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    discount_percent = models.IntegerField(default=0)
    status = models.IntegerField(choices=StatusProductType.choices, default=StatusProductType.draft.value)
    description = models.TextField()
    brif_description = models.TextField(null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
  
    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.title
    
    def get_discounted_price(self):
        """
        Calculate the price after discount.
        """
        if self.discount_percent > 0:
            discount_amount = (self.price * Decimal(self.discount_percent)) / 100
            return self.price - discount_amount
        return '{:,}'.format(round(self.price))
    

    
    def is_discount(self):
        return self.discount_percent != 0



class ProductImageModel(models.Model):
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    file = models.ImageField(upload_to='product/img/')

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

