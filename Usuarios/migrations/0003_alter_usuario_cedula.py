# Generated by Django 4.1 on 2022-09-27 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Usuarios", "0002_alter_usuario_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usuario",
            name="cedula",
            field=models.CharField(max_length=25, unique=True, verbose_name="Cedula"),
        ),
    ]