# Generated by Django 3.2.9 on 2022-12-27 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0049_auto_20221227_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudiante',
            name='telefono_facturar',
            field=models.IntegerField(blank=True, null=True, unique=True, verbose_name='teléfono a facturar'),
        ),
    ]