from django.shortcuts import render
from django.views.generic import CreateView, View, FormView, TemplateView, UpdateView, DeleteView, DetailView
from .filters import CampaignFilter, SubscriberFilter
from mailing.models import *
from mailing.tables import CampaignTable
from django_tables2 import SingleTableView
from django.db.models import Avg, Count, Min, Sum
from django.db.models import Q
from django.urls import reverse_lazy
from django.db.models.functions import Coalesce


class HomeView(View):

    def get(self, request, *args, **kwargs):
        campaigns = campaigns_info()

        campaign_filter = CampaignFilter(request.GET, queryset=campaigns)
        campaigns = campaign_filter.qs

        count_subs = Subscriber.objects.filter(campaign__in=campaigns).count()
        # table = CampaignTable(campaigns)
        return render(request, 'home.html',
                      {

                          'campaigns': campaigns,
                          'campaigns_filter': campaign_filter,
                          'count_subs': count_subs,
                          # 'table': table,

                      })

    def get_subs_count(self):
        return 1


def campaigns_info():
    unsubscribers = Count('subscriber', filter=Q(subscriber__unsubscribe=True))
    campaigns = Campaign.objects.annotate(subs_count=Count('subscriber'),
                                          sent=Coalesce(Sum('subscriber__sent'), 0),
                                          opened=Coalesce(Sum('subscriber__opened'), 0),
                                          clicks=Coalesce(Sum('subscriber__clicked'), 0),
                                          canceled=unsubscribers)
    return campaigns


def campaign_calc(pk):
    unsubscribers = Count('subscriber', filter=Q(subscriber__unsubscribe=True))
    campaign = Campaign.objects.filter(pk=pk). \
        annotate(subs_count=Count('subscriber'),
                 sent=Coalesce(Sum('subscriber__sent'), 0),
                 opened=Coalesce(Sum('subscriber__opened'), 0),
                 clicks=Coalesce(Sum('subscriber__clicked'), 0),
                 canceled=unsubscribers)
    return campaign


class CampaignPageView(DetailView):
    model = Campaign
    template_name = 'campaign.html'

    # def get(self, request, *args, **kwargs):
    #     emails = Email.objects.filter(campaign=kwargs['pk']).order_by('index')
    #     subscribers = Subscriber.objects.filter(campaign=kwargs['pk'])
    #     return render(request, 'campaign.html', {"emails":emails, "subscribers":subscribers})

    def get_context_data(self, **kwargs):
        emails = Email.objects.filter(campaign=kwargs['object'].pk).order_by('index')
        email_filter = CampaignFilter(self.request.GET, queryset=emails)
        emails = email_filter.qs
        subscribers = Subscriber.objects.filter(campaign=kwargs['object'].pk)
        subscribers_filter = SubscriberFilter(self.request.GET, queryset=subscribers)
        context = super().get_context_data(**kwargs)
        campaign_info = campaign_calc(kwargs['object'].pk)
        context['emails'] = emails
        context['email_filter'] = email_filter
        context['subscribers_filter'] = subscribers_filter
        context['subscribers'] = subscribers
        context['campaign_info'] = campaign_info
        return context


class CampaignCreateView(CreateView):
    template_name = 'edit.html'
    model = Campaign
    # form_class = EventForm
    fields = ['name', 'sender_name', 'sender_email', 'tags', 'status']
    success_url = '/manager/home/'
    extra_context = {
        "header": "יצירת קמפיין:",
        "comment": "",
        "btn_value": "מחק"

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


class EmailCreateView(CreateView):
    template_name = 'edit.html'
    model = Email
    # form_class = EventForm
    fields = ['campaign', 'header', 'text', 'html', 'index', 'delay_H', 'status']
    success_url = '/manager/home/'
    extra_context = {
        "header": "יצירת מייל:",
        "comment": "",
        "btn_value": "מחק"

    }

    template_name_suffix = '_update_form'


class EmailUpdateView(UpdateView):
    template_name = 'edit.html'
    model = Email
    # form_class = EventForm
    fields = ['campaign', 'header', 'text', 'html', 'index', 'delay_H', 'status']
    success_url = '/manager/home/'
    extra_context = {
        "header": "עריכת פרטי מייל:",
        "comment": "",

    }

    template_name_suffix = '_update_form'


class EmailDeleteView(DeleteView):
    template_name = 'edit.html'
    model = Email
    # form_class = EventForm
    # fields = "__all__"
    success_url = '/manager/home/'
    extra_context = {
        "header": "מחיקת מייל:",
        "comment": "האם את/ה בטוח ברצונך למחוק מייל זה?",

    }

    template_name_suffix = '_update_form'
