# Generated by Django 3.2.9 on 2022-11-02 17:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Picaderos', '0027_alter_estadoclase_dia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estadoclase',
            name='dia',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]