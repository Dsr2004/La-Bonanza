# Generated by Django 4.1 on 2022-10-06 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Estudiantes_Profesores", "0002_estudiante_aceptacontrato_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="estudiante", name="aceptaContrato", field=models.BooleanField(),
        ),
    ]