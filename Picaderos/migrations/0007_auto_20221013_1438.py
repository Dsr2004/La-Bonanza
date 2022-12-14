# Generated by Django 3.2.9 on 2022-10-13 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0007_auto_20221007_1230'),
        ('Picaderos', '0006_auto_20221013_1418'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clase',
            name='estudiante',
        ),
        migrations.AddField(
            model_name='clase',
            name='estudiante',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='Estudiantes_Profesores.estudiante'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='clase',
            name='profesor',
        ),
        migrations.AddField(
            model_name='clase',
            name='profesor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estudiantes_Profesores.profesor'),
        ),
    ]
