# Generated by Django 2.1.7 on 2019-03-17 06:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20190317_0639'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ad',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 3, 17, 6, 53, 57, 54867)),
        ),
    ]
