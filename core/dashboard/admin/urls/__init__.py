from django.urls import path,include
from .. import views

app_name = "admin"

urlpatterns = [
    path("",include('dashboard.admin.urls.profiles')),
    path("",include('dashboard.admin.urls.generals')),
    path("",include('dashboard.admin.urls.products'))
     
]