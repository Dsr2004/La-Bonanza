# Generated by Django 3.2.9 on 2022-10-21 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiantes_Profesores', '0012_auto_20221021_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro',
            name='finClase',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='horaClase',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='inicioClase',
            field=models.TextField(blank=True, null=True),
        ),
    ]