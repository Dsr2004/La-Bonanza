# Generated by Django 3.2.9 on 2022-10-07 03:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0003_alter_estudiante_aceptacontrato'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudiante',
            name='barrio_A',
            field=models.CharField(default=1, max_length=500, verbose_name='barrio de resdencia'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estudiante',
            name='ciudad_A',
            field=models.CharField(default=1, max_length=150, verbose_name='ciudad de residencia'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estudiante',
            name='direccion_A',
            field=models.CharField(default=1, max_length=500, verbose_name='direccion de residencia'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estudiante',
            name='fecha_inscripcion',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]