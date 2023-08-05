# Generated by Django 2.1.7 on 2020-07-15 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0004_auto_20200715_1925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='precolista',
            name='origem_delete',
        ),
        migrations.RemoveField(
            model_name='precolista',
            name='origem_edicao',
        ),
        migrations.RemoveField(
            model_name='precolista',
            name='origem_insercao',
        ),
        migrations.RemoveField(
            model_name='produto',
            name='id',
        ),
        migrations.AddField(
            model_name='produto',
            name='altura_ecommerce',
            field=models.DecimalField(decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='categoria_principal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='categoria_principal', to='produto.Categoria'),
        ),
        migrations.AddField(
            model_name='produto',
            name='cd_externo',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='cd_produto',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produto',
            name='descricao',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='descricao_ecommerce',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='imagem',
            field=models.FileField(default='produtos/caixa-nissei.jpg', upload_to='produtos'),
        ),
        migrations.AddField(
            model_name='produto',
            name='is_ecommerce',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='is_pbm',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='is_retencao_receita',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='is_venda_controlada',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='largura_ecommerce',
            field=models.DecimalField(decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='marca',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='marca', to='produto.Marca'),
        ),
        migrations.AddField(
            model_name='produto',
            name='marca_ecommerce',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='marca_ecommerce', to='produto.Marca'),
        ),
        migrations.AddField(
            model_name='produto',
            name='nm_ecommerce',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='nm_url_ecommerce',
            field=models.SlugField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='peso_ecommerce',
            field=models.DecimalField(decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='produto_pai',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='produto.Produto'),
        ),
        migrations.AddField(
            model_name='produto',
            name='profundidade_ecommerce',
            field=models.DecimalField(decimal_places=2, max_digits=14, null=True),
        ),
        migrations.DeleteModel(
            name='PrecoLista',
        ),
    ]
