from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasCustomerAccessPermission
from django.views.generic import TemplateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from dashboard.permissions import HasCustomerAccessPermission
from django.contrib.auth import views as auth_view
from django.contrib.messages.views import SuccessMessageMixin
from ..forms import  CustomerSecurityEditForm,CustomerProfileEditForm
from accounts.models import Profile
from django.contrib import messages



# Create your views here.
class CustomerDashboardHomeView(LoginRequiredMixin,HasCustomerAccessPermission,TemplateView):
    template_name = "dashboard/customer/home.html"


class CustomerSecurityEditView(LoginRequiredMixin,HasCustomerAccessPermission,SuccessMessageMixin,auth_view.PasswordChangeView):
    template_name = "dashboard/customer/profile/security-edit.html"  
    form_class = CustomerSecurityEditForm
    success_url = reverse_lazy("dashboard:customer:security-edit")
    success_message = "بروزرسانی رمز با موفقیت انجام شد"



class CustomerProfileEditView(LoginRequiredMixin,HasCustomerAccessPermission,SuccessMessageMixin,UpdateView):
    template_name = "dashboard/customer/profile/profile-edit.html"  
    form_class = CustomerProfileEditForm
    success_url = reverse_lazy("dashboard:customer:profile-edit")
    success_message = "بروزرسانی پروفایل با موفقیت انجام شد"
    
    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)
    

class CustomerProfileImageEditView(LoginRequiredMixin,HasCustomerAccessPermission,SuccessMessageMixin,UpdateView):
    http_method_names = ['post']
    model = Profile
    fields =['image']
     
    success_url = reverse_lazy("dashboard:customer:profile-edit")
    success_message = "بروزرسانی تصویر پروفایل با موفقیت انجام شد"

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def  form_invalid(self, form):
        return redirect(self.success_url)
       
