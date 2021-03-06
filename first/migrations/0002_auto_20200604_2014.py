# Generated by Django 3.0.6 on 2020-06-04 17:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='day',
            field=models.DateField(default=datetime.datetime(2020, 6, 4, 17, 14, 22, 494066, tzinfo=utc), verbose_name='Day of the event'),
        ),
        migrations.AlterField(
            model_name='note',
            name='public_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 4, 17, 14, 22, 493370, tzinfo=utc), verbose_name='The publication date'),
        ),
    ]
