from django.shortcuts import render, HttpResponse
from django.views.generic import CreateView, View, FormView, TemplateView
from .funcs.funcs import send_mass_html_mail
from .models import Email, Subscriber, Campaign
from .forms import SubscriberForm
from ipware import get_client_ip
import base64
import random
from django.views.decorators.cache import cache_control
from .funcs.funcs import handel_mailing


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


# TODO insert data to pixel
class PixelView(View):

    @cache_control(must_revalidate=True, max_age=60)
    def get(self, request):
        data = request.GET
        email = Email.objects.get(pk=data['email_pk'])
        subscriber = Subscriber.objects.get(pk=data['subscriber_pk'])

        email.opened += 1
        email.save()
        subscriber.opened += 1
        subscriber.save()

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
        PIXEL_GIF_DATA = base64.b64decode(
            b"R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")
        return HttpResponse(PIXEL_GIF_DATA, content_type='image/gif')
