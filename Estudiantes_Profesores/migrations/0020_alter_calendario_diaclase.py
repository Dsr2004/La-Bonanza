# Generated by Django 3.2.9 on 2022-10-25 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0019_asistencia_picadero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendario',
            name='diaClase',
            field=models.CharField(choices=[('1', 'Lunes'), ('2', 'Martes'), ('3', 'Miércoles'), ('4', 'Jueves'), ('5', 'Viernes'), ('6', 'Sábado'), ('0', 'Domingo')], max_length=10),
        ),
    ]