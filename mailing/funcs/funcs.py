from mailing.models import Email
from django.db.models import Min
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.template.loader import get_template


# TODO add try
def handel_mailing(subscriber, index=1, extra_context={}):
    """
    :param subscriber:
    :param index: the place of the email in the sending order. default=1 and not 0 in favor of 'zero day' email
    :return:
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

    subscriber.send_email_date = datetime.now() + timedelta(hours=email.delay_H)
    subscriber.save()
