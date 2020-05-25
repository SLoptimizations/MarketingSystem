from django.urls import path, re_path
from mailing import views

app_name = 'mailing'

urlpatterns = [

    path('pixel/open/pixel.gif/', views.PixelView.as_view(), name='pixel'),
    path('thanks/', views.thanks_view, name='thanks'),
    path('<str:campaign_pk>/', views.RegistrationView.as_view(), name='register'),
]