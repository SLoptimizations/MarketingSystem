# Generated by Django 3.0.3 on 2020-05-24 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='status',
            field=models.CharField(choices=[('1', 'on'), ('0', 'of')], default=0, max_length=2),
        ),
    ]
