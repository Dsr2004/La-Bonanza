# Generated by Django 4.1 on 2022-10-06 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Usuarios", "0004_alter_usuario_celular"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usuario",
            name="apellidos",
            field=models.CharField(max_length=25, verbose_name="Apellidos"),
        ),
        migrations.AlterField(
            model_name="usuario",
            name="celular",
            field=models.CharField(max_length=10, unique=True, verbose_name="Celular"),
        ),
        migrations.AlterField(
            model_name="usuario",
            name="nombres",
            field=models.CharField(max_length=50, verbose_name="Nombre completo"),
        ),
        migrations.AlterField(
            model_name="usuario",
            name="usuario",
            field=models.CharField(
                max_length=50, unique=True, verbose_name="Nombre de Usuario"
            ),
        ),
    ]
