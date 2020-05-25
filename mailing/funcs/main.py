from django.core.mail import get_connection, EmailMultiAlternatives
from django.template.loader import get_template
from mailing.models import Email



headers = {
    "Return-Receipt-To": 'SLoptimizations@gmail.com',
    "Disposition-Notification-To": 'SLoptimizations@gmail.com',
}


def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None,
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

        html_content = get_template(f"{email.html}.html").render(context={'facebook': 'fachebook'})
        # new_html_email_text = adapt_html(
        #     html_content, extra_metadata={"customer_id": 1},
        #     click_tracking=True, open_tracking=True)
        message.attach_alternative(html_content, 'text/html')
        messages.append(message)
        print('success')
    return connection.send_messages(messages)


# new_email = Email.objects.all()
# message1 = (new_email, ['SLoptimizations@gmail.com'])
# message2 = (new_email, ['SLoptimizations@gmail.com'])
#
# send_mass_html_mail((message1, message2))
