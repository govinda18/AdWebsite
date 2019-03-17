# Generated by Django 2.1.7 on 2019-03-17 06:39

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20190317_0533'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_code', models.CharField(max_length=50)),
                ('expiry', models.DateField()),
                ('profile_ref', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.Client')),
            ],
        ),
        migrations.AlterField(
            model_name='ad',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 3, 17, 6, 39, 28, 227488)),
        ),
    ]
