# Generated by Django 4.1 on 2022-12-20 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Estudiantes_Profesores", "0037_alter_estudiante_documento"),
    ]

    operations = [
        migrations.AlterField(
            model_name="estudiante",
            name="comprobante_documento_identidad",
            field=models.BooleanField(
                default=True, verbose_name="tiene comprobante de documento de identidad"
            ),
        ),
        migrations.AlterField(
            model_name="estudiante",
            name="comprobante_seguro_medico",
            field=models.BooleanField(
                default=True, verbose_name="tiene comprobante de seguro medico"
            ),
        ),
    ]
