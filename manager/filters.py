from mailing.models import *
from django_filters import DateFilter, FilterSet, CharFilter

class CampaignFilter(FilterSet):

    class Meta:
        model = Campaign
        fields = ['name','status']
