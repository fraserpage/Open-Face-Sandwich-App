# Generated by Django 3.2.4 on 2021-07-12 22:41

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0003_rename_slice_slices'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Slices',
            new_name='Photo',
        ),
    ]