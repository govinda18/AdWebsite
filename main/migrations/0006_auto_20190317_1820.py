# Generated by Django 2.1.7 on 2019-03-17 18:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190317_0653'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='ad',
            name='services',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='ad',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 3, 17, 18, 20, 13, 23651)),
        ),
    ]
