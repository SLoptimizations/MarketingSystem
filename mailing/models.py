from django.db import models
from django.core.validators import EmailValidator
from taggit.managers import TaggableManager
import datetime
from django.urls import reverse

# Create your models here.
# TODO add pixel class

class Campaign(models.Model):
    STATUS_OPTIONS = (
        ('1', 'on'),
        ('0', 'of'),
    )
    name = models.CharField(max_length=60, blank=False)
    sender_name = models.CharField(max_length=60, blank=False)
    sender_email = models.EmailField(max_length=100, blank=False, validators=[EmailValidator])
    tags = TaggableManager()
    status = models.CharField(max_length=2, choices=STATUS_OPTIONS, default=0)
    subscribers = models.IntegerField(default=0)
    unsubscribed = models.IntegerField(default=0)
    sum_sent = models.IntegerField(default=0)
    sum_opened = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("mailing:register", kwargs={'campaign_pk': self.pk})






class Email(models.Model):
    STATUS_OPTIONS = (
        ('1', 'on'),
        ('0', 'of'),
    )

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    header = models.CharField(max_length=60, blank=False)
    text = models.TextField()
    html = models.CharField(max_length=60)
    # delay = models.DurationField(default=datetime.timedelta(days=0, hours=0))
    delay_H = models.IntegerField(default=0)
    index = models.PositiveIntegerField(default=None, null=True)
    status = models.CharField(max_length=2, choices=STATUS_OPTIONS, default=0)
    # sent = models.IntegerField(default=0)
    # opened = models.IntegerField(default=0)
    # clicked = models.IntegerField(default=0)

    def __str__(self):
        return f"{str(self.index)}-{self.header}"


class Subscriber(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    name = models.CharField(max_length=60, blank=False)
    email = models.EmailField(max_length=100, blank=False, validators=[EmailValidator])
    unsubscribe = models.BooleanField(default=0)
    ip = models.CharField(max_length=16, default='', blank=True)# InetAddressField()
    sent = models.IntegerField(default=0)
    opened = models.IntegerField(default=0)
    clicked = models.IntegerField(default=0)

    next_email = models.ForeignKey(Email, on_delete=models.CASCADE, null= True)
    # next_email_index = models.PositiveIntegerField(default=0, null=True)
    send_email_date = models.DateField(null=True)

    def __str__(self):
        return self.name
