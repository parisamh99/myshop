from django.shortcuts import render,redirect
from django.views.generic import FormView,TemplateView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from .permissions import HasCustomerAccessPermission
from order.models import UserAddressModel,OrderModel,OrderItemModel,CouponModel
from cart.models import CartModel
from order.forms import CheckOutForm
from cart.cart import CartSession
from django.urls import reverse_lazy,reverse
from decimal import Decimal
from django.http import JsonResponse
from django.utils import timezone





class OrderCheckoutView(LoginRequiredMixin,HasCustomerAccessPermission,FormView):
    template_name = 'order/checkout.html'
    form_class = CheckOutForm
    success_url = reverse_lazy('payment:request_payment')

    def form_valid(self, form):
     user = self.request.user
     address = form.cleaned_data['address_id']  # الان آبجکت UserAddressModel هست
     coupon = form.cleaned_data.get('coupon')  # الان آبجکت CouponModel یا None

     cart = CartModel.objects.get(user=user)
     cart_items = cart.cart_items.all()

     order = OrderModel.objects.create(
        user=user,
        address=address.address,
        state=address.state,
        city=address.city,
        zip_code=address.zip_code,
    )
     

     for item in cart_items:
        OrderItemModel.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.get_price(),
        )

    # محاسبه قیمت پایه
     base_total = order.calculate_total_price()
     final_total = base_total

    # اعمال تخفیف
     if coupon:
        discount = (base_total * Decimal(coupon.discount_percent)) / Decimal('100')
        final_total -= discount
        order.coupon = coupon
        coupon.used_by.add(user)  # اضافه کردن کاربر به لیست استفاده‌کنندگان

     order.total_price = final_total
     order.save()

    # پاکسازی سبد
     cart.cart_items.all().delete()
     CartSession(self.request.session).clear()

     #return super().form_valid(form)
     return redirect(
        reverse('payment:request_payment', kwargs={'order_id': order.id}))

    
    def form_invalid(self, form):
        print(self.request.POST)
        return super().form_invalid(form)
     

    def get_form_kwargs(self):
        kwargs = super(OrderCheckoutView,self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs 

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_cart = CartSession(self.request.session)
        session_cart.merge_session_cart_in_db(self.request.user)
        cart = CartModel.objects.get(user=self.request.user)
        context["addresses"] = UserAddressModel.objects.filter(
            user=self.request.user)
        total_price = cart.calculate_total_price()
        context["total_price"] = total_price
        context["total_tax"] = round((total_price * 9)/100)
        return context


class OrderCompeletedView(LoginRequiredMixin,HasCustomerAccessPermission,TemplateView):
    template_name = 'order/compeleted.html'


class OrderValidateCouponView(LoginRequiredMixin,HasCustomerAccessPermission,View):
   
    def post(self,request,*args,**kwargs):
       code = request.POST.get('code')
       user = self.request.user
       status_code = 200
       message = "کد تخفیف با موفقیت ثبت شد"
       total_price = 0
       total_tax = 0
       
       try:
            coupon = CouponModel.objects.get(code=code)
       except CouponModel.DoesNotExist:
            status_code,message = 404,("کد تخفیف اشتباه است")
       else:

        if coupon.used_by.count() >= coupon.limited_usage:
            status_code,message = 403,("تعداد استفاده از کد تخفیف به پایان رسیده")

        elif coupon.expiration_date and coupon.expiration_date < timezone.now():
            status_code,message = 403,("کد تخفیف منقضی شده است")

        elif user in coupon.used_by.all():
            status_code,message = 403,("شما قبلاً از این کد استفاده کرده‌اید")
        else:
            cart = CartModel.objects.get(user=self.request.user)
            total_price = cart.calculate_total_price()
            discount_amount = (total_price * Decimal(coupon.discount_percent)) / 100
            total_price_after_discount = total_price - discount_amount 
            total_tax = (total_price * Decimal('9')) / Decimal('100')


       return JsonResponse ({"message":message, "total_price":total_price_after_discount,"total_tax":total_tax}, status=status_code)