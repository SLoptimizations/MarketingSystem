from django.urls import path, re_path
from manager import views
from django.conf.urls import url
app_name = 'manager'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('campaign/<str:pk>/', views.CampaignPageView.as_view(), name='campaign'),
    path('campaign-update/<str:pk>/', views.CampaignUpdateView.as_view(), name='campaign-update'),
    path('campaign-delete/<str:pk>/', views.CampaignDeleteView.as_view(), name='campaign-delete'),
    path('campaign-create/', views.CampaignCreateView.as_view(), name='campaign-create'),
    path('email-update/<str:pk>/', views.EmailUpdateView.as_view(), name='email-update'),
    path('email-delete/<str:pk>/', views.EmailDeleteView.as_view(), name='email-delete'),
    path('email-create/', views.EmailCreateView.as_view(), name='email-create'),
]