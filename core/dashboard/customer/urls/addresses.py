from django.urls import path,include
from . import views


urlpatterns = [ 
    path('address/create/',views.CustomerAddressCreateView.as_view(), name="address-create"),
    path('address/list/',views.CustomerAddressListView.as_view(), name="address-list"),
    path('address/<int:pk>/edit/',views.CustomerAddressEditeView.as_view(), name="address-edit"),
    path('address/<int:pk>/delete/',views.CustomerAddressDeleteView.as_view(), name="address-delete"),
]