from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasCustomerAccessPermission
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasCustomerAccessPermission
from django.contrib.auth import views as auth_view





# Create your views here.
class CustomerDashboardHomeView(LoginRequiredMixin,HasCustomerAccessPermission,TemplateView):
    template_name = "dashboard/customer/home.html"