# Generated by Django 3.0.3 on 2020-05-26 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0008_campaign_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='next_email_index',
            field=models.PositiveIntegerField(default=1, null=True),
        ),
    ]
