# Generated by Django 2.0 on 2018-09-19 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rank_item', '0002_auto_20180919_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companycategory',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Category name'),
        ),
    ]
