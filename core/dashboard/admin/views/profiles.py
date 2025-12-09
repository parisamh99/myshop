from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.auth import views as auth_view
from django.contrib.messages.views import SuccessMessageMixin
from ..forms import AdminSecurityEditForm,AdminProfileEditForm
from accounts.models import Profile
from django.contrib import messages
from dashboard.admin.forms import *





class AdminSecurityEditView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,auth_view.PasswordChangeView):
    template_name = "dashboard/admin/profile/security-edit.html"  
    form_class = AdminSecurityEditForm
    success_url = reverse_lazy("dashboard:admin:security-edit")
    success_message = "بروزرسانی رمز با موفقیت انجام شد"



class AdminProfileEditView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,UpdateView):
    template_name = "dashboard/admin/profile/profile-edit.html"  
    form_class = AdminProfileEditForm
    success_url = reverse_lazy("dashboard:admin:profile-edit")
    success_message = "بروزرسانی پروفایل با موفقیت انجام شد"
    
    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)
    

class AdminProfileImageEditView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,UpdateView):
    http_method_names = ['post']
    model = Profile
    fields =['image']
     
    success_url = reverse_lazy("dashboard:admin:profile-edit")
    success_message = "بروزرسانی تصویر پروفایل با موفقیت انجام شد"

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def  form_invalid(self, form):
        return redirect(self.success_url)
       
