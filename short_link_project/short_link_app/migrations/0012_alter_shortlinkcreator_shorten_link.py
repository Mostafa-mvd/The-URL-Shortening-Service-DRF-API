# Generated by Django 3.2.8 on 2021-10-28 10:08

import django.core.validators
from django.db import migrations, models
import short_link_app.utils


class Migration(migrations.Migration):

    dependencies = [
        ('short_link_app', '0011_alter_shortlinkcreator_shorten_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortlinkcreator',
            name='shorten_link',
            field=models.CharField(default=short_link_app.defaults.generate_token, max_length=18, unique=True, validators=[
                                   django.core.validators.RegexValidator('[\\w-]{8, 18}')]),
        ),
    ]
