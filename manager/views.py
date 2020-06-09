from django.shortcuts import render
from django.views.generic import CreateView, View, FormView, TemplateView
from .filters import CampaignFilter
from mailing.models import *

class HomeView(View):
    def get(self, request, *args, **kwargs):
        campaigns = Campaign.objects.all()
        campaign_filter = CampaignFilter(request.GET, queryset=campaigns)
        campaigns = campaign_filter.qs

        count_subs = Subscriber.objects.filter(campaign__in=campaigns).count()
        return render(request, 'home.html',
                      {

                          'campaigns': campaigns,
                          'campaigns_filter': campaign_filter,
                          'count_subs':count_subs,


                      })
    def get_subs_count(self):
        return 1
