# Generated by Django 2.1.7 on 2020-08-06 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0026_auto_20200805_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avaliacao',
            name='dat_delete',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cartao',
            name='dat_delete',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cartaobandeira',
            name='dat_delete',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cartaobandeiraparcela',
            name='dat_delete',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='dat_delete',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clientetermo',
            name='dat_delete',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cupom',
            name='dat_delete',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='dat_delete',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='favorito',
            name='dat_delete',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='receita',
            name='dat_delete',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='termo',
            name='dat_delete',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
