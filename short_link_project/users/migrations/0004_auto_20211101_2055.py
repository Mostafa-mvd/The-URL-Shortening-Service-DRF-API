# Generated by Django 3.2.8 on 2021-11-01 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userotpcode_user_secret_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userotpcode',
            name='otp_code',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='userotpcode',
            name='user_secret_key',
            field=models.CharField(max_length=250),
        ),
    ]