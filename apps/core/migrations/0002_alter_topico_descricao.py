# Generated by Django 5.1.6 on 2025-03-21 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topico',
            name='descricao',
            field=models.TextField(max_length=250),
        ),
    ]
