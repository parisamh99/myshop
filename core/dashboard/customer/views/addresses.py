from django.views.generic import UpdateView,ListView,DeleteView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from dashboard.permissions import HasCustomerAccessPermission
from django.core.exceptions import FieldError
from django.contrib.messages.views import SuccessMessageMixin
from ..forms import AddressForm
from order.models import UserAddressModel




class CustomerAddressListView(LoginRequiredMixin,HasCustomerAccessPermission,ListView):
    template_name = 'dashboard/customer/addresses/address-list.html'
       

    def get_queryset(self):
        queryset = UserAddressModel.objects.all()
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q) 
        if order_by := self.request.GET.get("order_by"):
            try:
             queryset = queryset.order_by(order_by)
            except FieldError: 
             pass

        return queryset
   

class CustomerAddressEditeView(LoginRequiredMixin,HasCustomerAccessPermission,SuccessMessageMixin,UpdateView):  
    template_name = 'dashboard/customer/addresses/address-edit.html'
    form_class = AddressForm
    success_message = "ویرایش با موفقیت انجام شد"

    def get_queryset(self):
        return UserAddressModel.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("dashboard:customer:address-edit", kwargs={"pk":self.get_object().pk})
    

class CustomerAddressDeleteView(LoginRequiredMixin,HasCustomerAccessPermission,SuccessMessageMixin,DeleteView):
    template_name = 'dashboard/customer/addresses/address-delete.html'
    success_message = "حذف محصول با موفقیت انجام شد"

    def get_queryset(self):
        return UserAddressModel.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("dashboard:customer:address-list")
    


class CustomerAddressCreateView(LoginRequiredMixin,HasCustomerAccessPermission,SuccessMessageMixin,CreateView):  
    template_name = 'dashboard/customer/addresses/address-create.html'
    form_class = AddressForm

    def get_queryset(self):
        return UserAddressModel.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    success_message = "ایجاد آدرس با موفقیت انجام شد"

    def get_success_url(self):
        return reverse_lazy("dashboard:customer:address-list")
