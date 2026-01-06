from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('request_payment/<int:order_id>/',views.StartPaymentView,name='request_payment'),
    path('verify_payment/<int:order_id>/',views.VerifyPaymentView,name='verify_payment'),

]
