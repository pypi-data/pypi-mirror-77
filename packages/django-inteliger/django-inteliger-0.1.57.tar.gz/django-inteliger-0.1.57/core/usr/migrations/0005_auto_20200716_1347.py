# Generated by Django 2.1.7 on 2020-07-16 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usr', '0004_auto_20200716_1205'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grupo',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='grupouser',
            options={'managed': True},
        ),
    ]
