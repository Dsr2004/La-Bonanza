# Generated by Django 3.2.9 on 2022-10-13 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0007_auto_20221007_1230'),
        ('Picaderos', '0007_auto_20221013_1438'),
    ]

    operations = [
        migrations.RenameField(
            model_name='infopicadero',
            old_name='clase',
            new_name='clases',
        ),
        migrations.AlterField(
            model_name='clase',
            name='estudiante',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Estudiantes_Profesores.registro'),
        ),
    ]
