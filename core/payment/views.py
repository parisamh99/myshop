from django.shortcuts import render
from django.views.generic import View
from core import settings
from order.models import OrderModel
from django.shortcuts import redirect
from django.http import HttpResponse
import requests
from django.urls import reverse

ZARINPAL_REQUEST_URL = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZARINPAL_STARTPAY_URL = "https://sandbox.zarinpal.com/pg/StartPay/"
ZARINPAL_VERIFY_URL = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"


        
def StartPaymentView(request,order_id):
    order = OrderModel.objects.get(
        id=order_id,
        user=request.user
    )
    amount = int(order.get_price())
    callback_url= callback_url = request.build_absolute_uri(
     reverse('payment:verify_payment', kwargs={'order_id': order.id}))

    description = "خرید از فروشگاه"

    data = {
        "merchant_id": settings.MERCHANT_ID,
        "amount": amount,
        "callback_url": callback_url,
        "description":description,
    }
    response = requests.post(ZARINPAL_REQUEST_URL, json=data)
    result = response.json()
    print(result)
    if result["data"]["code"] == 100:
        Authority = result["data"]["authority"] 
        return redirect(ZARINPAL_STARTPAY_URL + Authority)
    

def VerifyPaymentView(request,order_id):
    order = OrderModel.objects.get(
        id=order_id,
        user=request.user
    )
    amount = int(order.get_price())
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')

    if status != "OK":
        return HttpResponse("پرداخت لغو شد")

    data = {
        "merchant_id": settings.MERCHANT_ID,
        "amount": amount,
        "authority":authority, 
    }
    response = requests.post(ZARINPAL_VERIFY_URL,json=data)
    result = response.json()
    print(result)

    if result["data"]["code"] in [100, 101]:
        ref_id = result["data"]["ref_id"]
        return HttpResponse("پرداخت موفق ✅")
    return HttpResponse("پرداخت ناموفق ❌")
