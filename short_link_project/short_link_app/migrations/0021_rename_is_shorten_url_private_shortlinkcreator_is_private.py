# Generated by Django 3.2.8 on 2021-10-28 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('short_link_app', '0020_rename_redirected_times_shortlinkcreator_times_of_redirected'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shortlinkcreator',
            old_name='is_shorten_url_private',
            new_name='is_private',
        ),
    ]
