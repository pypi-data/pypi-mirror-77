# Generated by Django 2.2.3 on 2019-11-28 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jbank', '0041_auto_20191127_0559'),
    ]

    operations = [
        migrations.AddField(
            model_name='wsediconnection',
            name='bank_encryption_cert_file',
            field=models.FileField(blank=True, upload_to='certs', verbose_name='bank encryption cert file'),
        ),
    ]
