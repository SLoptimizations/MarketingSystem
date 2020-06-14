from mailing.models import *
from django_filters import DateFilter, FilterSet, CharFilter

class CampaignFilter(FilterSet):

    class Meta:
        model = Campaign
        fields = ['name','status']


class EmailFilter(FilterSet):

    class Meta:
        model = Email
        fields = ['campaign','header','index','status']

class SubscriberFilter(FilterSet):

    class Meta:
        model = Subscriber
        fields = ['name','unsubscribe']
