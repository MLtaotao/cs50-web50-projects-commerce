# Generated by Django 3.1.4 on 2020-12-15 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20201214_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='sell_button',
            field=models.BooleanField(default=False),
        ),
    ]
