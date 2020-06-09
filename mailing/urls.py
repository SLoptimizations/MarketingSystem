from django.urls import path, re_path
from mailing import views
from django.conf.urls import url
app_name = 'mailing'

urlpatterns = [
    path('pixel/open/pixel.gif/', views.PixelView.as_view(), name='pixel'),

    url(r"^pixel/open/(?P<path>[\w=-]+)/$", views.MyOpenTrackingView.as_view(),
        name="open_tracking"),
    url(r"^pixel/click/(?P<path>[\w=-]+)/$", views.MyClickTrackingView.as_view(),
            name="click_tracking"),
    # path('pixel/open/', views.MyOpenTrackingView.as_view(), name='pixel'),
    # path('pixel/click/', views.MyOpenTrackingView.as_view(), name='pixel'),
    path('pixel/webhook/', views.PixelView.as_view(), name='pixel_webhook'),
    path('thanks/', views.thanks_view, name='thanks'),
    path('unsubscribe/<subscriber_pk>/', views.UnsubscribeView.as_view(), name='unsubscribe'),
    path('<str:campaign_pk>/', views.RegistrationView.as_view(), name='register'),


]
