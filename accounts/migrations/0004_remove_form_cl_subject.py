# Generated by Django 3.1.4 on 2021-02-10 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210210_1936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form_cl',
            name='subject',
        ),
    ]
