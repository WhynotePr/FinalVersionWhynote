# Generated by Django 3.0.6 on 2020-06-05 09:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0005_auto_20200605_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='day',
            field=models.DateField(default=datetime.datetime(2020, 6, 5, 9, 47, 41, 351594, tzinfo=utc), verbose_name='Day of the event'),
        ),
        migrations.AlterField(
            model_name='note',
            name='public_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 5, 9, 47, 41, 350993, tzinfo=utc), verbose_name='The publication date'),
        ),
    ]
