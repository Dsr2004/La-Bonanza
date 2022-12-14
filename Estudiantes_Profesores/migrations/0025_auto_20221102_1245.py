# Generated by Django 3.2.9 on 2022-11-02 17:45

import Estudiantes_Profesores.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0024_auto_20221102_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiante',
            name='documento_A',
            field=models.FileField(upload_to=Estudiantes_Profesores.models.guardar_documento),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='exoneracion',
            field=models.FileField(upload_to=Estudiantes_Profesores.models.guardar_exoneracion),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='seguro_A',
            field=models.FileField(upload_to=Estudiantes_Profesores.models.guardar_seguro),
        ),
    ]
