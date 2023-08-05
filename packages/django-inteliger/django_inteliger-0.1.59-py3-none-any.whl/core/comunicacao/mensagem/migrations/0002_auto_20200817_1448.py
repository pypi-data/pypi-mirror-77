# Generated by Django 2.1.7 on 2020-08-17 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mensagem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensagem',
            name='conteudo',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mensagem',
            name='nm_descritivo',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='mensagem',
            name='variaveis',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mensagemlog',
            name='destinatario',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='mensagemlog',
            name='mensagem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mensagem.Mensagem'),
        ),
        migrations.AlterField(
            model_name='mensagemlog',
            name='retorno',
            field=models.TextField(blank=True, null=True),
        ),
    ]
