# Generated by Django 3.1.5 on 2021-09-07 03:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='author',
            new_name='user',
        ),
    ]
