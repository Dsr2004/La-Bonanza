# Generated by Django 3.2.9 on 2022-10-28 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0023_calendario_estado'),
        ('Picaderos', '0014_remove_infopicadero_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clase',
            name='estudiante',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Estudiantes_Profesores.calendario'),
        ),
    ]
