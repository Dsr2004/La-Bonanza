# Generated by Django 3.2.9 on 2022-10-25 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0020_alter_calendario_diaclase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registro',
            name='inicioClase',
        ),
    ]
