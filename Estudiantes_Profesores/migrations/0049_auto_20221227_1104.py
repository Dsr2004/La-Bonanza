# Generated by Django 3.2.9 on 2022-12-27 16:04

import Estudiantes_Profesores.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0048_alter_asistencia_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudiante',
            name='firma',
            field=models.FileField(blank=True, null=True, upload_to=Estudiantes_Profesores.models.guardar_firma, validators=[Estudiantes_Profesores.models.validar_extencion_archivo]),
        ),
        migrations.AddField(
            model_name='estudiante',
            name='nombrefirma',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='nombre de la persona que está firmando'),
        ),
    ]
