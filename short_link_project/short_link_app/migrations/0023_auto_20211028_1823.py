# Generated by Django 3.2.8 on 2021-10-28 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('short_link_app', '0022_alter_shortlinkcreator_token'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShortLinkCreator',
            new_name='ShortLink',
        ),
        migrations.AlterModelOptions(
            name='shortlink',
            options={'ordering': ['-created_time'], 'verbose_name': 'ShortLink', 'verbose_name_plural': 'ShortLinks'},
        ),
    ]
