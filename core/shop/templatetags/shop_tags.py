from django import template
from shop.models import StatusProductType, ProductModel, ProductCategoryModel
register = template.Library()

@register.inclusion_tag('includes/latest-products.html')
def show_latest_products():
    latest_products = ProductModel.objects.filter(status=StatusProductType.publish.value).order_by("-created_date")[:8]
    return {"latest_products": latest_products}



@register.inclusion_tag('includes/similar-products.html')
def show_similar_products(product):
    product_categories = product.product_category.all()
    similar_products = ProductModel.objects.filter(status=StatusProductType.publish.value, proudct_category__in=product_categories).order_by("-created_date")[:4]
    return {"similar_products": similar_products}



@register.inclusion_tag('includes/similar-products.html')
def show_similar_products(product):
    product_categories = product.proudct_category.all()
    similar_products = ProductModel.objects.filter(
        status=StatusProductType.publish.value,
        proudct_category__in=product_categories
    ).exclude(id=product.id).distinct().order_by("-created_date")[:4]

    return {"similar_products": similar_products}
