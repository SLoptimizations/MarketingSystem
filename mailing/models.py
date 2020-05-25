from django.db import models
from django.core.validators import EmailValidator
from taggit.managers import TaggableManager

# Create your models here.


class Campaign(models.Model):
    name = models.CharField(max_length=60, blank=False)
    sender_name = models.CharField(max_length=60, blank=False)
    sender_email = models.EmailField(max_length=100, blank=False, validators=[EmailValidator])
    tags = TaggableManager()
    unsubscribed = models.IntegerField(default=0)
    sum_sent = models.IntegerField(default=0)
    sum_opened = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Email(models.Model):
    STATUS_OPTIONS = (
        ('1', 'on'),
        ('0', 'of'),
    )

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    header = models.CharField(max_length=60, blank=False)
    text = models.TextField()
    html = models.CharField(max_length=60)
    # delay = models.DurationField(default=)
    delay_H = models.IntegerField(default=0)
    index = models.IntegerField(default=0)
    status = models.CharField(max_length=2, choices=STATUS_OPTIONS, default=0)

    def __str__(self):
        return self.header

class Subscriber(models.Model):
    # CAMPAIGN_LIST = Campaign.objects.values('name')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    name = models.CharField(max_length=60, blank=False)
    email = models.EmailField(max_length=100, blank=False, validators=[EmailValidator])
    unsubscribe = models.BooleanField(default=0)
    # url_id = models.CharField(max_length=7, default='', blank=True)
    # ip = models.CharField(max_length=16, default='', blank=True)# InetAddressField()
    sent = models.IntegerField(default=0)
    opened = models.IntegerField(default=0)
    clicked = models.IntegerField(default=0)

    next_email_index = models.ForeignKey(Email, on_delete=models.CASCADE)
    send_email_date = models.DateField()

    def __str__(self):
        return self.name
