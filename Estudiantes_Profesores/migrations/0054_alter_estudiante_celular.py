# Generated by Django 3.2.9 on 2023-01-06 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0053_auto_20230106_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiante',
            name='celular',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='número de celular'),
        ),
    ]
