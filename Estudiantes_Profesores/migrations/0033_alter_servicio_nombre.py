# Generated by Django 4.1 on 2022-11-09 20:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Estudiantes_Profesores", "0032_remove_servicio_tipo_servicio_tipo_clase"),
    ]

    operations = [
        migrations.AlterField(
            model_name="servicio",
            name="nombre",
            field=models.CharField(max_length=55, verbose_name="Nombre del servicio"),
        ),
    ]