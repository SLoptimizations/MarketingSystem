from django.db.models import Min
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.template.loader import get_template
from django.core.mail import get_connection, EmailMultiAlternatives
from mailing.models import Email, Campaign, Subscriber
import datetime
from cryptography.fernet import Fernet
import pytracking
from pytracking.html import adapt_html


main_site = ' https://15135e24bb9c.ngrok.io/'



# TODO add try , maybe add to subscriber model class
def handel_mailing(subscriber, index=1, extra_context={}):
    """
    :param subscriber:
    :param index: the place of the email in the sending order. default=1 and not 0 in favor of 'zero day' email
    :return: sets email sending data. if delay_H == 0 sending mail instantly
    """
    # subscriber.next_email_index = index
    # subscriber.save()

    email = Email.objects.get(campaign=subscriber.campaign, index=index)
    # subscriber.next_email_index = index
    # subscriber.save()
    context = {'email_pk': email.pk, 'subscriber_pk': subscriber.pk}
    context.update(extra_context)
    html = get_template(f"{email.html}.html").render(context=context)
    if email.delay_H == 0:
        send_mail(
            subject=email.header,
            message=email.text,
            from_email=email.campaign.sender_email,
            recipient_list=[subscriber.email],
            fail_silently=False,
            html_message=html
        )
        email.sent += 1
        email.save()
        subscriber.sent += 1
        # subscriber.next_email_index = index + 1

        # TODO check if no more emails
        # set next email
        email = Email.objects.get(campaign=subscriber.campaign, index=index+1)

    subscriber.next_email = email
    subscriber.send_email_date = datetime.datetime.now() + timedelta(hours=email.delay_H)
    subscriber.save()


# TODO : change sender name
# TODO : schedual mailing
headers = {
    "Return-Receipt-To": 'SLoptimizations@gmail.com',
    "Disposition-Notification-To": 'SLoptimizations@gmail.com',
}


def send_mass_html_mail(datatuple, context=None, fail_silently=False, user=None, password=None,
                        connection=None):
    """
    Given a datatuple of (Email, recipient_list),
    sends each message to each recipient list.
    Returns the number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    """
    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently)

    messages = []
    for email, recipient in datatuple:
        sender = f'{email.campaign.sender_name}<{email.campaign.sender_email}>'

        for pk, email_adr in recipient:
            message = EmailMultiAlternatives(email.header,
                                             email.text,
                                             sender,
                                             [email_adr],
                                             headers=headers)
            if context is None:
                context = {}
            context['pk'] = pk

            html_content = get_template(f"{email.html}.html").render(context=context)
            html_email_text = "..."
            key = Fernet.generate_key()
            new_html_email_text = adapt_html(
                html_content, extra_metadata={"customer_id": pk,"email_pk": email.pk},
                click_tracking=False, open_tracking=True, base_open_tracking_url=f'{main_site}pixel/open/', base_click_tracking_url=f'{main_site}pixel/click/')
            message.attach_alternative(new_html_email_text, 'text/html')
            messages.append(message)
            print(email_adr)
    return connection.send_messages(messages)


# TODO
def send_emails():
    """
    Sends all scheduled email

    """
    subscribers = Subscriber.objects.filter(unsubscribe=0, send_email_date=datetime.date.today())
    emails_data = list(Subscriber.objects.values_list('next_email', flat=True))
    emails = Email.objects.filter(pk__in=emails_data)
    datatuple = ()
    for email in emails:
        recipient_tuple = list(subscribers.filter(next_email=email).values_list('pk', 'email'))
        datatuple += ((email, recipient_tuple),)

    send_mass_html_mail(datatuple)



# send_emails()

# open_tracking_url = pytracking.get_open_tracking_url(
#     {"customer_id": 1}, base_open_tracking_url= f"{main_site}pixel/open/",
#     webhook_url="http://requestb.in/123", include_webhook_url=True)
# print(open_tracking_url)