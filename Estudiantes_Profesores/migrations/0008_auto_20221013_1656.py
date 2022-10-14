# Generated by Django 3.2.9 on 2022-10-13 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0007_auto_20221007_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiante',
            name='celular',
            field=models.IntegerField(blank=True, null=True, verbose_name='numero de celular'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='correo electronico'),
        ),
    ]
