import django_tables2 as tables
from .models import Campaign

class CampaignTable(tables.Table):
    subscriber__count = tables.Column()

    class Meta:
        model = Campaign
        template_name = "django_tables2/bootstrap.html"
        fields = ("name","sender_name", 'status','subscribers')