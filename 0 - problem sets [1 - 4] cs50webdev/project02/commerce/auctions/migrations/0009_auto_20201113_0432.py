# Generated by Django 3.1.2 on 2020-11-13 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20201111_0315'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='owner',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='listing',
            name='time',
            field=models.CharField(default='2020-11-13 04:32:17', max_length=30),
        ),
    ]