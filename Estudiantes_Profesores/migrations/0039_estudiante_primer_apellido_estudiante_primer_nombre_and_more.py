# Generated by Django 4.1 on 2022-12-20 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "Estudiantes_Profesores",
            "0038_alter_estudiante_comprobante_documento_identidad_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="estudiante",
            name="primer_apellido",
            field=models.CharField(
                default="", max_length=50, verbose_name="Primer apellido"
            ),
        ),
        migrations.AddField(
            model_name="estudiante",
            name="primer_nombre",
            field=models.CharField(
                default="", max_length=50, verbose_name="Primer nombre"
            ),
        ),
        migrations.AddField(
            model_name="estudiante",
            name="segundo_apellido",
            field=models.CharField(
                default="", max_length=50, verbose_name="Segundo apellido"
            ),
        ),
        migrations.AddField(
            model_name="estudiante",
            name="segundo_nombre",
            field=models.CharField(
                blank=True,
                default="",
                max_length=50,
                null=True,
                verbose_name="Segundo nombre",
            ),
        ),
        migrations.AlterField(
            model_name="estudiante",
            name="tipo_clase",
            field=models.CharField(
                choices=[("1", "Clase esporadica"), ("2", "Mensualidad")], max_length=15
            ),
        ),
        migrations.AlterField(
            model_name="servicio",
            name="tipo_clase",
            field=models.CharField(
                choices=[("1", "Clase esporadica"), ("2", "Mensualidad")], max_length=15
            ),
        ),
    ]
