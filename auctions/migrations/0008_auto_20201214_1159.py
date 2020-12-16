# Generated by Django 3.1.4 on 2020-12-14 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_watchlist'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='watchlist',
            constraint=models.UniqueConstraint(fields=('user', 'watchlist'), name='user-auction'),
        ),
    ]