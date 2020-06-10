from django.shortcuts import render
from django.views.generic import CreateView, View, FormView, TemplateView
from .filters import CampaignFilter
from mailing.models import *
from mailing.tables import CampaignTable
from django_tables2 import SingleTableView
from django.db.models import Avg, Count, Min, Sum
from django.db.models import Q
class HomeView(View):

    def get(self, request, *args, **kwargs):
        unsubscribers = Count('subscriber', filter=Q(subscriber__unsubscribe=True))
        campaigns = Campaign.objects.annotate(subs_count=Count('subscriber'),
                                              sent=Sum('subscriber__sent'),
                                              opened=Sum('subscriber__opened'),
                                              clicks=Sum('subscriber__clicked'),
                                              canceled=unsubscribers)
        # campaigns = Campaign.objects.annotate(canceled = Count('subscriber')).filter(canceled__gt=True)



        campaign_filter = CampaignFilter(request.GET, queryset=campaigns)
        # campaigns = campaign_filter.qs

        count_subs = Subscriber.objects.filter(campaign__in=campaigns).count()
        table = CampaignTable(campaigns)
        return render(request, 'home.html',
                      {

                          'campaigns': campaigns,
                          'campaigns_filter': campaign_filter,
                          'count_subs':count_subs,
                          'table':table,


                      })
    def get_subs_count(self):
        return 1

def campaigns_info(campaigns):

    subs = Subscriber.objects.filter(campaign__in=campaigns)
    # for campaign in campaigns:


    # for campaign in campaigns:

