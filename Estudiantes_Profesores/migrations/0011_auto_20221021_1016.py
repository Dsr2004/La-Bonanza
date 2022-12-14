# Generated by Django 3.2.9 on 2022-10-21 15:16

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0010_calendario_registro_calendario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro',
            name='diaClase',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('1', 'Lunes'), ('2', 'Martes'), ('3', 'Miércoles'), ('4', 'Jueves'), ('5', 'Viernes'), ('6', 'Sábado'), ('0', 'Domingo')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='finClase',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='horaClase',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='inicioClase',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='profesor',
            field=models.ForeignKey(blank=True, db_column='profesor_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estudiantes_Profesores.profesor', verbose_name='profesor del estudiante'),
        ),
    ]
