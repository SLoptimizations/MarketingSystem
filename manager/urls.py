from django.urls import path, re_path
from manager import views
from django.conf.urls import url
app_name = 'manager'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
]