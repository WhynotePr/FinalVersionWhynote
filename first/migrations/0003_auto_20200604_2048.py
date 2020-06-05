# Generated by Django 3.0.6 on 2020-06-04 17:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0002_auto_20200604_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='day',
            field=models.DateField(default=datetime.datetime(2020, 6, 4, 17, 48, 53, 634028, tzinfo=utc), verbose_name='Day of the event'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Final time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='note',
            name='public_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 4, 17, 48, 53, 633372, tzinfo=utc), verbose_name='The publication date'),
        ),
    ]
