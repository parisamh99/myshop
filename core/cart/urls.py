from django.urls import path,re_path
from . import views


app_name = "cart"

urlpatterns = [
    path("session/add-product/",views.SessionAddProductView.as_view(),name='session_product_add'),
    path("session/cart/summary/",views.SessionCartSummary.as_view(),name="session_cart_summary"),
    path("session/update-product/",views.SessionUpdateProductView.as_view(),name='session_product_update'),
    path("session/remove-product/",views.SessionRemoveProductView.as_view(),name='session_product_remove'),
]
