# Generated by Django 3.1.4 on 2021-02-14 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0011_auto_20210214_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tests',
            name='created_at',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='tests',
            name='planned',
            field=models.DateField(null=True),
        ),
    ]
