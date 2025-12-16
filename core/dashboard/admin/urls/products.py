from django.urls import path
from .. import views




urlpatterns = [
    path('products/list/', views.AdminProductsListView.as_view(), name="product-list"),
    path('products/<int:pk>/edit/', views.AdminProductsEditView.as_view(), name="product-edit"),
    path('products/<int:pk>/delete/', views.AdminProductsDeleteView.as_view(), name="product-delete"),
    path('products/create/', views.AdminProductCreateView.as_view(), name="product-create")
]