# Generated by Django 3.2.9 on 2022-09-29 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0002_alter_asistencia_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudiante',
            name='tipo_clase',
            field=models.CharField(choices=[('1', 'Clase puntual'), ('2', 'Mensualidad')], default=1, max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='estado',
            field=models.CharField(choices=[('1', 'Clase puntual'), ('2', 'Mensualidad')], max_length=15),
        ),
    ]
