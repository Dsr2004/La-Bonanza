# Generated by Django 3.2.9 on 2022-12-29 03:15

import Estudiantes_Profesores.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0050_estudiante_telefono_facturar'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudiante',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to=Estudiantes_Profesores.models.guardar_imagen, verbose_name='Imagen del estudiante'),
        ),
    ]
