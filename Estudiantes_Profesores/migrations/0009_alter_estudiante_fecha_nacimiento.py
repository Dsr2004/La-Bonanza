# Generated by Django 3.2.9 on 2022-10-14 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0008_auto_20221013_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiante',
            name='fecha_nacimiento',
            field=models.DateField(verbose_name='Fecha de nacimiento'),
        ),
    ]