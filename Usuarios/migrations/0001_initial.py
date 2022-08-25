# Generated by Django 4.1 on 2022-08-24 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Usuario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "usuario",
                    models.CharField(
                        max_length=15, unique=True, verbose_name="Usuario"
                    ),
                ),
                (
                    "nombres",
                    models.CharField(max_length=15, verbose_name="Nombre de usuario"),
                ),
                (
                    "celular",
                    models.CharField(max_length=10, verbose_name="Celular del usuario"),
                ),
                (
                    "apellidos",
                    models.CharField(max_length=25, verbose_name="Apellido de usuario"),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="Correo Electrónico"
                    ),
                ),
                (
                    "estado",
                    models.BooleanField(
                        default=True, verbose_name="Estado del usuario"
                    ),
                ),
                ("administrador", models.BooleanField(default=False)),
            ],
            options={"db_table": "usuarios",},
        ),
    ]
