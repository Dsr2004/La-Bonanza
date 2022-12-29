# Generated by Django 3.2.9 on 2022-12-29 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0005_alter_usuario_apellidos_alter_usuario_celular_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='Usuarios/', verbose_name='Imagen de usuario'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='cedula',
            field=models.CharField(max_length=25, unique=True, verbose_name='Cédula'),
        ),
    ]
