from django.urls import path, re_path
from manager import views
from django.conf.urls import url
app_name = 'manager'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('campaign-update/<str:pk>/', views.CampaignUpdateView.as_view(), name='campaign-update'),
    path('campaign-delete/<str:pk>/', views.CampaignDeleteView.as_view(), name='campaign-delete'),
    path('campaign-create/', views.CampaignCreateView.as_view(), name='campaign-create'),
]