# Generated by Django 4.1.3 on 2022-12-22 17:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Picaderos', '0028_alter_estadoclase_dia'),
    ]

    operations = [
        migrations.AddField(
            model_name='picadero',
            name='creado',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]