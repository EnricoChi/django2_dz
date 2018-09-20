# Generated by Django 2.0 on 2018-09-20 08:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20180920_0156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 22, 8, 59, 59, 376913, tzinfo=utc), verbose_name='Key validity'),
        ),
    ]
