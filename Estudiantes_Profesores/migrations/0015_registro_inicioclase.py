# Generated by Django 3.2.9 on 2022-10-21 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0014_auto_20221021_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='registro',
            name='inicioClase',
            field=models.TextField(blank=True, null=True),
        ),
    ]