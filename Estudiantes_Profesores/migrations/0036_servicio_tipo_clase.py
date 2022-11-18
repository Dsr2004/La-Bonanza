# Generated by Django 3.2.9 on 2022-11-17 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0035_remove_servicio_tipo_clase'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='tipo_clase',
            field=models.CharField(choices=[('1', 'Clase puntual'), ('2', 'Mensualidad')], default=3, max_length=15),
            preserve_default=False,
        ),
    ]
