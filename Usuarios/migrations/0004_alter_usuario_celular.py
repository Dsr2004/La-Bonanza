# Generated by Django 4.1 on 2022-09-27 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Usuarios", "0003_alter_usuario_cedula"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usuario",
            name="celular",
            field=models.CharField(
                max_length=10, unique=True, verbose_name="Celular del usuario"
            ),
        ),
    ]
