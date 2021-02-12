# Generated by Django 3.1.4 on 2021-02-11 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='form',
            field=models.ManyToManyField(related_name='teacher_classes', to='students.Classes'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='form_teacher',
            field=models.CharField(blank=True, default=False, max_length=5),
        ),
    ]