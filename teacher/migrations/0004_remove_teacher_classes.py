# Generated by Django 3.1.4 on 2021-02-11 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_auto_20210211_0958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='classes',
        ),
    ]