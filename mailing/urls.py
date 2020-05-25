from django.urls import path, re_path
from mailing import views

app_name = 'mailing'

urlpatterns = [
    path('', views.RegistrationView.as_view(), name='index'),
    path('pixel/<str:pixel>.gif/', views.PixelView.as_view(), name='pixel'),
]