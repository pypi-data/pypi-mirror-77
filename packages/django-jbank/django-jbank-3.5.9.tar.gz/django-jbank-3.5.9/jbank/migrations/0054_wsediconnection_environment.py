# Generated by Django 2.2.3 on 2019-11-30 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jbank', '0053_wsediconnection_target_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='wsediconnection',
            name='environment',
            field=models.CharField(default='PRODUCTION', max_length=32, verbose_name='environment'),
        ),
    ]
