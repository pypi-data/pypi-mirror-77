# Generated by Django 2.1.7 on 2020-07-17 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0014_auto_20200716_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='qtd_max_venda_ecommerce',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='qtd_min_venda_ecommerce',
            field=models.IntegerField(default=1, null=True),
        ),
    ]
