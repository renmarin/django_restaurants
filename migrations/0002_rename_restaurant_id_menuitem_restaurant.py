# Generated by Django 3.2.8 on 2021-10-25 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menuitem',
            old_name='restaurant_id',
            new_name='restaurant',
        ),
    ]
