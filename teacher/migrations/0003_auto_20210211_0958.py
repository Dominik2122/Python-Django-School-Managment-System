# Generated by Django 3.1.4 on 2021-02-11 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_auto_20210211_0954'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='form',
            new_name='classes',
        ),
    ]
