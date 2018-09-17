# Generated by Django 2.0 on 2018-09-16 23:51

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180916_2109'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.PositiveSmallIntegerField(choices=[(0, ''), (1, 'Male'), (2, 'Female')], default=0, verbose_name='Gender')),
                ('organization', models.CharField(blank=True, max_length=255, verbose_name='Organization')),
            ],
        ),
        migrations.AlterField(
            model_name='account',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 18, 23, 51, 21, 813222, tzinfo=utc), verbose_name='Key validity'),
        ),
        migrations.AddField(
            model_name='accountinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
