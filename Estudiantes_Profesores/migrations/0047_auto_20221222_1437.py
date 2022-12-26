# Generated by Django 3.2.9 on 2022-12-22 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0046_remove_profesor_trabaja_sabado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiante',
            name='tipo_clase',
            field=models.CharField(choices=[('1', 'Clase esporádica'), ('2', 'Mensualidad')], max_length=15),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='tipo_clase',
            field=models.CharField(choices=[('1', 'Clase esporádica'), ('2', 'Mensualidad')], max_length=15),
        ),
    ]