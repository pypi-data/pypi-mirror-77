# Generated by Django 2.1.7 on 2020-07-31 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20200728_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='cep',
            name='tipo_cep',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
