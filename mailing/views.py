from django.shortcuts import render, HttpResponse
from django.views.generic import CreateView, View, FormView, TemplateView
# from .funcs.funcs import send_mass_html_mail
from .models import Email, Subscriber, Campaign
from .forms import SubscriberForm
from ipware import get_client_ip
import base64
import random
from django.views.decorators.cache import cache_control
from .funcs.funcs import handel_mailing
from pytracking import Configuration
from pytracking.django import OpenTrackingView, ClickTrackingView

# Create your views here.

def thanks_view(request):
    return render(request, 'thanks.html')

class ThanksView(TemplateView):
    template_name = 'thanks.html'

class RegistrationView(FormView):
    template_name = 'index.html'
    form_class = SubscriberForm
    success_url = '/thanks/'

    # def get(self, request, *args, **kwargs):
    #     campagin = Campaign.objects.get(pk=self.kwargs['campaign_pk'])
    #     self.template_name = Campaign


    def form_valid(self, form):
        campagin = Campaign.objects.get(pk=self.kwargs['campaign_pk'])
        subscriber = form.save(commit=False)
        subscriber.campaign = campagin
        subscriber.save()
        campagin.subscribers += 1
        campagin.save()
        handel_mailing(subscriber)
        return super().form_valid(form)

PIXEL_GIF_DATA = base64.b64decode(b"R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")

# TODO insert data to pixel
class PixelView(View):

    @cache_control(must_revalidate=True, max_age=60)
    def get(self, request):
        # data = request.GET
        # email = Email.objects.get(pk=data['email_pk'])
        # subscriber = Subscriber.objects.get(pk=data['subscriber_pk'])
        #
        # email.opened += 1
        # email.save()
        # subscriber.opened += 1
        # subscriber.save()

        ip, is_routable = get_client_ip(request)
        if ip is None:
            print("Unable to get the client's IP address")
        else:
            print(f"We got the client's IP address: {ip}")

            if is_routable:
                print("The client's IP address is publicly routable on the Internet")
            else:
                print(" The client's IP address is private")

        print('pixel:')
        print(request)

        return HttpResponse(PIXEL_GIF_DATA, content_type='image/gif')

class PixelOpenView(View):
    """
    Update open email data
    """
    @cache_control(must_revalidate=True, max_age=60)
    def get(self, request):
        data = request.GET
        email = Email.objects.get(pk=data['email_pk'])
        subscriber = Subscriber.objects.get(pk=data['subscriber_pk'])

        email.opened += 1
        email.save()
        subscriber.opened += 1
        subscriber.save()

        return HttpResponse(PIXEL_GIF_DATA, content_type='image/gif')


class MyOpenTrackingView(OpenTrackingView):

    def notify_tracking_event(self, tracking_result):
        """
        Get pixel data and update Subscriber and Email
        :param tracking_result:
                tracking_result.request_data["user_agent"]
                tracking_result.request_data["user_ip"]
        :return:
        """

        # send_tracking_result_to_queue(tracking_result)
        subscriber = Subscriber.objects.get(pk=tracking_result.metadata['customer_id'])
        email = Email.objects.get(pk=tracking_result.metadata['email_pk'])
        subscriber.opened += 1
        subscriber.ip = tracking_result.request_data["user_ip"]
        subscriber.save()
        email.opened += 1
        email.save()
        print(tracking_result.metadata)
        print(tracking_result.request_data["user_agent"])
        print(tracking_result.request_data["user_ip"])

    def notify_decoding_error(self, exception):
        """
        Called when the tracking link cannot be decoded
        """
        # logger.log(exception)
        print('error')

    def get_configuration(self):
        main_site = 'https://6f4ca8b1d675.ngrok.io/'
        return Configuration(webhook_url=f'{main_site}pixel/webhook/',
                             base_open_tracking_url=f'{main_site}pixel/open/',
                             base_click_tracking_url=f'{main_site}pixel/click/',
                             )
        # return Configuration()


class MyClickTrackingView(ClickTrackingView):

    def notify_tracking_event(self, tracking_result):
        """
                Get pixel data and update Subscriber and Email
                :param tracking_result:
                        tracking_result.request_data["user_agent"]
                        tracking_result.request_data["user_ip"]
                :return:
                """

        # send_tracking_result_to_queue(tracking_result)
        subscriber = Subscriber.objects.get(pk=tracking_result.metadata['customer_id'])
        email = Email.objects.get(pk=tracking_result.metadata['email_pk'])
        subscriber.clicked += 1
        # subscriber.ip = tracking_result.request_data["user_ip"]
        subscriber.save()
        email.clicked += 1
        email.save()
        print(tracking_result.metadata)
        print(tracking_result.request_data["user_agent"])
        print(tracking_result.request_data["user_ip"])

    def notify_decoding_error(self, exception):
        # Called when the tracking link cannot be decoded
        # Override this to, for example, log the exception
        # logger.log(exception)
        print('error2')

    def get_configuration(self):
        # By defaut, fetchs the configuration parameters from the Django
        # settings. You can return your own Configuration object here if
        # you do not want to use Django settings.
        return Configuration()


class UnsubscribeView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'unsubscribe.html')

    def post(self, request, *args, **kwargs):
        data = request.POST
        if data.get('yes'):
            subscriber = Subscriber.objects.get(pk=kwargs['subscriber_pk'])
            subscriber.unsubscribe = '1'
            subscriber.save()
            text = "You are now unsubscribed."

        else:
            text = "You are still subscribed. have a grate day! "

        return render(request, 'unsubscribe_thanks.html', context={'text': text})