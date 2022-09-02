# Generated by Django 4.1 on 2022-09-02 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Estudiantes_Profesores", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="registro",
            name="diaClase",
            field=models.CharField(
                choices=[
                    (1, "Lunes"),
                    (2, "Martes"),
                    (3, "Miércoles"),
                    (4, "Jueves"),
                    (5, "Viernes"),
                    (6, "Sábado"),
                    (7, "Domingo"),
                ],
                default=1,
                max_length=1,
            ),
            preserve_default=False,
        ),
    ]
