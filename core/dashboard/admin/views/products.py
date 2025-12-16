from django.views.generic import UpdateView,ListView,DeleteView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from shop.models import ProductCategoryModel, ProductModel, StatusProductType
from dashboard.permissions import HasAdminAccessPermission
from django.contrib import messages
from dashboard.admin.forms import *
from django.core.exceptions import FieldError
from django.contrib.messages.views import SuccessMessageMixin
from ..forms import ProductForm





class AdminProductsListView(LoginRequiredMixin,HasAdminAccessPermission,ListView):
    template_name = 'dashboard/admin/products/product-list.html'
    paginate_by = 9
    
        

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)
   
    

    def get_queryset(self):
        queryset = ProductModel.objects.all()
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(proudct_category__id = category_id)  
        if min_price := self.request.GET.get('min_price'):
            queryset = queryset.filter(price__gte=min_price)
        if max_price := self.request.GET.get('max_price'):
            queryset = queryset.filter(price__lte=max_price) 
        if order_by := self.request.GET.get("order_by"):
            try:
             queryset = queryset.order_by(order_by)
            except FieldError: 
             pass

        return queryset


    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        context["categories"] = ProductCategoryModel.objects.all()
        return context
    


class AdminProductsEditView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,UpdateView):  
    template_name = 'dashboard/admin/products/product-edit.html'
    queryset = ProductModel.objects.all()
    form_class = ProductForm
    success_message = "ویرایش با موفقیت انجام شد"

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-edit", kwargs={"pk":self.get_object().pk})
    

class AdminProductsDeleteView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,DeleteView):
    template_name = 'dashboard/admin/products/product-delete.html'
    queryset = ProductModel.objects.all()
    success_message = "حذف محصول با موفقیت انجام شد"
    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-list")

class AdminProductCreateView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,CreateView):  
    template_name = 'dashboard/admin/products/product-create.html'
    queryset = ProductModel.objects.all()
    form_class = ProductForm
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    success_message = "ایجاد محصول با موفقیت انجام شد"

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-list")
