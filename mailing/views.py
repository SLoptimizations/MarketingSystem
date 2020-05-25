from django.shortcuts import render, HttpResponse
from django.views.generic import CreateView, View
from .funcs.main import send_mass_html_mail
from .models import Email
from ipware import get_client_ip
import base64
import random
from django.views.decorators.cache import cache_control
# Create your views here.


class RegistrationView(View):
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        new_email = Email.objects.all()
        message1 = (new_email[0], ['SLoptimizations@gmail.com'])
        message2 = (new_email[0], ['SLoptimizations@gmail.com'])
        pix_id = random.randint(100, 999)
        send_mass_html_mail((message1, message2), context={'pix_id': pix_id})

        return render(request, 'tanku.html')

# TODO insert data to user
class PixelView(View):

    @cache_control(must_revalidate=True, max_age=60)
    def get(self, request, pixel):



        ip, is_routable = get_client_ip(request)
        if ip is None:
         print(" Unable to get the client's IP address")
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


