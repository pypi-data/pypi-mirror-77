# Generated by Django 2.2.3 on 2019-11-27 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jbank', '0039_auto_20191127_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='wsediconnection',
            name='signing_key_file',
            field=models.FileField(blank=True, upload_to='certs', verbose_name='signing key file'),
        ),
    ]
