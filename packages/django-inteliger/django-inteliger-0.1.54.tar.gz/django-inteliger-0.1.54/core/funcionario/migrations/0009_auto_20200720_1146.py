# Generated by Django 2.1.7 on 2020-07-20 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionario', '0008_auto_20200716_1451'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='funcionariologin',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='cargo',
            name='origem_delete_tipo',
            field=models.CharField(default='USR.PROFILE', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cargo',
            name='origem_edicao_tipo',
            field=models.CharField(default='USR.PROFILE', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cargo',
            name='origem_insercao_tipo',
            field=models.CharField(default='USR.PROFILE', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='origem_delete_tipo',
            field=models.CharField(default='USR.PROFILE', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='origem_edicao_tipo',
            field=models.CharField(default='USR.PROFILE', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='origem_insercao_tipo',
            field=models.CharField(default='USR.PROFILE', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='funcionariologin',
            name='origem_delete_tipo',
            field=models.CharField(default='USR.PROFILE', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='funcionariologin',
            name='origem_edicao_tipo',
            field=models.CharField(default='USR.PROFILE', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='funcionariologin',
            name='origem_insercao_tipo',
            field=models.CharField(default='USR.PROFILE', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='funcionariologin',
            name='origem_tipo',
            field=models.CharField(default='USR.PROFILE', max_length=200, null=True),
        ),
    ]
