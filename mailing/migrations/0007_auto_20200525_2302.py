# Generated by Django 3.0.3 on 2020-05-25 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0006_auto_20200525_2236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='delay',
        ),
        migrations.AddField(
            model_name='email',
            name='delay_H',
            field=models.IntegerField(default=0),
        ),
    ]