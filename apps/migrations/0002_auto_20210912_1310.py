# Generated by Django 3.2.7 on 2021-09-12 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='diagnostico',
            options={'verbose_name': 'Diagnóstico', 'verbose_name_plural': 'Diagnósticos'},
        ),
        migrations.AddField(
            model_name='diagnostico',
            name='serv',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='apps.servicio'),
            preserve_default=False,
        ),
    ]
