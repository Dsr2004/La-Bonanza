# Generated by Django 3.2.9 on 2022-10-28 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Picaderos', '0016_rename_estudiante_clase_clase'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clase',
            old_name='clase',
            new_name='calendario',
        ),
    ]
