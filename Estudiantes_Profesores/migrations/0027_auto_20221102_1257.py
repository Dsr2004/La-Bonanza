# Generated by Django 3.2.9 on 2022-11-02 17:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0026_auto_20221102_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiante',
            name='cedula_madre',
            field=models.IntegerField(blank=True, null=True, unique=True, validators=[django.core.validators.MaxValueValidator(20)], verbose_name='numero de cedula de la madre'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='cedula_padre',
            field=models.IntegerField(blank=True, null=True, unique=True, validators=[django.core.validators.MaxValueValidator(20)], verbose_name='numero de cedula del padre'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='celular',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(20)], verbose_name='numero de celular'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='celular_madre',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(20)], verbose_name='numero de celular de la madre'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='celular_padre',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(20)], verbose_name='numero de celular del padre '),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='documento',
            field=models.IntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(20)], verbose_name='numero de documento'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='telefono_contactoE',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(20)], verbose_name='telefono del contacto de emergencia'),
        ),
    ]
