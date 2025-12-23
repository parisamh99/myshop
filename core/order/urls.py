from django.urls import path,re_path
from . import views

app_name = "order"

urlpatterns = [
    path('checkout/',views.OrderCheckoutView.as_view(), name="checkout"),
    path('compeleted/',views.OrderCompeletedView.as_view(), name="compeleted"),
    path('validate-coupon/',views.OrderValidateCouponView.as_view(), name="validate-coupon"),
]    