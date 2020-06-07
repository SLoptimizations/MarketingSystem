from django.db.models import Min
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.template.loader import get_template
from django.core.mail import get_connection, EmailMultiAlternatives
from mailing.models import Email, Campaign, Subscriber
import datetime


# TODO add try
def handel_mailing(subscriber, index=1, extra_context={}):
    """
    :param subscriber:
    :param index: the place of the email in the sending order. default=1 and not 0 in favor of 'zero day' email
    :return: sets email sending data. if delay_H == 0 sending mail instantly
    """
    subscriber.next_email_index = index
    subscriber.save()

    email = Email.objects.get(campaign=subscriber.campaign, index=subscriber.next_email_index)
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
        subscriber.next_email_index = index + 1

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
        message = EmailMultiAlternatives(email.header,
                                         email.text,
                                         email.campaign.sender_email,
                                         recipient,
                                         headers=headers)

        html_content = get_template(f"{email.html}.html").render(context=context)
        message.attach_alternative(html_content, 'text/html')
        messages.append(message)
        print('success')
    return connection.send_messages(messages)


def send_emails():
    # campaigns = Campaign.objects.filter(status='1')
    subscribers = Subscriber.objects.filter(unsubscribe=0, send_email_date=datetime.date.today())
    emails_data = subscribers.values_list('campaign_id', 'next_email_index').distinct()

    # emails = Email.objects.filter(campaign__status='1', status='1')
    # emails = Email.objects.extra(where=["('campaign_id','index') in %s"],params=[tuple(emails_data)])
    for campaign_id, index in emails_data:
        email = Email.objects.filter(campaign_id=campaign_id, index=index, status='1')
        subs = subscribers.filter()


send_emails()
