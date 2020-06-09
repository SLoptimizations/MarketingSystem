from mailing.models import Email, Subscriber, Campaign
from .funcs import send_emails
import schedule

# def send_scheduled_emails():
#

def main():
    schedule.every().day.at("09:00").do(send_emails())
    print("i")

if __name__ == "__main__":
    main()