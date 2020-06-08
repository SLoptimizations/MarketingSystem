from mailing.models import Email, Subscriber, Campaign
from .funcs import send_emails
import schedule

# def send_scheduled_emails():
#

def main():
    schedule.every().day.at("00:00").do(bedtime)
    print("i")

if __name__ == "__main__":
    main()