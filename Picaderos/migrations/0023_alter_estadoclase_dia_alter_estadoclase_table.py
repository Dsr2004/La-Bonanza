# Generated by Django 4.1 on 2022-10-30 19:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Picaderos", "0022_alter_estadoclase_dia_alter_estadoclase_table"),
    ]

    operations = [
        migrations.AlterField(
            model_name="estadoclase",
            name="dia",
            field=models.DateField(
                default=datetime.datetime(2022, 10, 30, 14, 53, 19, 522699)
            ),
        ),
        migrations.AlterModelTable(
            name="estadoclase",
            table="HistorialClases",
        ),
    ]
