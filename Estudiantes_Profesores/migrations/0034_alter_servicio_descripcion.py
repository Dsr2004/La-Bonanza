# Generated by Django 4.1 on 2022-11-09 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Estudiantes_Profesores", "0033_alter_servicio_nombre"),
    ]

    operations = [
        migrations.AlterField(
            model_name="servicio",
            name="descripcion",
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                verbose_name="Descripción del servicio",
            ),
        ),
    ]
