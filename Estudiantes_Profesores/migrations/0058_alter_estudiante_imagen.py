# Generated by Django 4.1.3 on 2023-01-10 15:52

import Estudiantes_Profesores.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0057_merge_0055_auto_20230106_1424_0056_auto_20230105_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiante',
            name='imagen',
            field=models.ImageField(blank=True, default='Default/usuario_estudiante.jpg', null=True, upload_to=Estudiantes_Profesores.models.guardar_imagen, verbose_name='Imagen del estudiante'),
        ),
    ]