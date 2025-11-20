from django.contrib import admin
from shop.models import ProductCategoryModel,ProductImageModel,ProductModel

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","title","status","stock","price","discount_percent","created_date")


@admin.register(ProductCategoryModel)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("id","title","created_date")  


@admin.register(ProductImageModel)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "created_date")


