# Generated by Django 3.1.4 on 2020-12-13 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20201212_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='auction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.auction'),
        ),
    ]