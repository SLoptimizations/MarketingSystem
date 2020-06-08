from django.urls import path, re_path, reverse_lazy
from mailing import views

app_name = 'test_app'


urlpatterns = [


    path('thanks/', views.ThanksView.as_view(template_name=f'{app_name}/thanks.html'), name='thanks'),
    path('<str:campaign_pk>/',
         views.RegistrationView.as_view(
             template_name=f'{app_name}/index.html',
             success_url=reverse_lazy(f'{app_name}:thanks')),
         name='register'),
]

