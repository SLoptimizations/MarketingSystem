from django.contrib import admin
from .models import Campaign, Email, Subscriber
# Register your models here.

admin.site.register(Campaign)
admin.site.register(Email)
admin.site.register(Subscriber)