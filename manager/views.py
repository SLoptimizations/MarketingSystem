from django.shortcuts import render
from django.views.generic import CreateView, View, FormView, TemplateView, UpdateView, DeleteView
from .filters import CampaignFilter
from mailing.models import *
from mailing.tables import CampaignTable
from django_tables2 import SingleTableView
from django.db.models import Avg, Count, Min, Sum
from django.db.models import Q
from django.urls import reverse_lazy
from django.db.models.functions import Coalesce


class HomeView(View):

    def get(self, request, *args, **kwargs):
        unsubscribers = Count('subscriber', filter=Q(subscriber__unsubscribe=True))
        campaigns = Campaign.objects.annotate(subs_count=Count('subscriber'),
                                              sent=Coalesce(Sum('subscriber__sent'), 0),
                                              opened=Coalesce(Sum('subscriber__opened'), 0),
                                              clicks=Coalesce(Sum('subscriber__clicked'), 0),
                                              canceled=unsubscribers)

        campaign_filter = CampaignFilter(request.GET, queryset=campaigns)
        campaigns = campaign_filter.qs

        count_subs = Subscriber.objects.filter(campaign__in=campaigns).count()
        table = CampaignTable(campaigns)
        return render(request, 'home.html',
                      {

                          'campaigns': campaigns,
                          'campaigns_filter': campaign_filter,
                          'count_subs': count_subs,
                          'table': table,

                      })

    def get_subs_count(self):
        return 1


def campaigns_info(campaigns):
    subs = Subscriber.objects.filter(campaign__in=campaigns)
    # for campaign in campaigns:

    # for campaign in campaigns:


class CampaignCreateView(CreateView):
    template_name = 'edit.html'
    model = Campaign
    # form_class = EventForm
    fields = ['name', 'sender_name','sender_email', 'tags', 'status']
    success_url = '/manager/home/'
    extra_context = {
        "header": "יצירת קמפיין:",
        "comment": "",
        "btn_value":"מחק"

    }

    template_name_suffix = '_update_form'

class CampaignUpdateView(UpdateView):
    template_name = 'edit.html'
    model = Campaign
    # form_class = EventForm
    fields = "__all__"
    success_url = '/manager/home/'
    extra_context = {
        "header": "עריכת פרטי קמפיין:",
        "comment": "",

    }

    template_name_suffix = '_update_form'


class CampaignDeleteView(DeleteView):
    template_name = 'edit.html'
    model = Campaign
    # form_class = EventForm
    # fields = "__all__"
    success_url = '/manager/home/'
    extra_context = {
        "header": "מחיקת קמפיין:",
        "comment": "האם את/ה בטוח ברצונך למחוק קמפיין זה?",

    }

    template_name_suffix = '_update_form'
