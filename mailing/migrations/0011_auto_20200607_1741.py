# Generated by Django 3.0.3 on 2020-06-07 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0010_auto_20200526_1456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriber',
            name='next_email_index',
        ),
        migrations.AddField(
            model_name='subscriber',
            name='next_email',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.Email'),
        ),
    ]