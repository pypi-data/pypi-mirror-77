# Generated by Django 2.1.7 on 2020-07-15 22:31

import compositefk.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200715_1925'),
        ('produto', '0007_auto_20200715_1931'),
    ]

    operations = [
        migrations.CreateModel(
            name='Desconto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dat_insercao', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_edicao', models.DateTimeField(auto_now=True, null=True)),
                ('dat_delete', models.DateTimeField(null=True)),
                ('usr_insercao', models.IntegerField(null=True)),
                ('usr_edicao', models.IntegerField(null=True)),
                ('usr_delete', models.IntegerField(null=True)),
                ('origem_insercao_codigo', models.CharField(max_length=200, null=True)),
                ('origem_insercao_tipo', models.CharField(default='USR.ORIGEM', max_length=200, null=True)),
                ('origem_edicao_codigo', models.CharField(max_length=200, null=True)),
                ('origem_edicao_tipo', models.CharField(default='USR.ORIGEM', max_length=200, null=True)),
                ('origem_delete_codigo', models.CharField(max_length=200, null=True)),
                ('origem_delete_tipo', models.CharField(default='USR.ORIGEM', max_length=200, null=True)),
                ('status', models.BooleanField(default=True, null=True)),
                ('qtd_desc', models.IntegerField(null=True)),
                ('valor_desc', models.DecimalField(decimal_places=2, max_digits=14, null=True)),
                ('per_desc', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('dat_ini', models.DateField(null=True)),
                ('dat_fim', models.DateField(null=True)),
                ('prioridade', models.IntegerField(null=True)),
                ('origem_delete', compositefk.fields.CompositeForeignKey(null=True, null_if_equal=[], on_delete=django.db.models.deletion.DO_NOTHING, related_name='produto_desconto_origem_delete', to='core.Tipo', to_fields={'codigo': compositefk.fields.LocalFieldValue('origem_delete_codigo'), 'tipo': compositefk.fields.LocalFieldValue('origem_delete_tipo')})),
                ('origem_edicao', compositefk.fields.CompositeForeignKey(null=True, null_if_equal=[], on_delete=django.db.models.deletion.DO_NOTHING, related_name='produto_desconto_origem_edicao', to='core.Tipo', to_fields={'codigo': compositefk.fields.LocalFieldValue('origem_edicao_codigo'), 'tipo': compositefk.fields.LocalFieldValue('origem_edicao_tipo')})),
                ('origem_insercao', compositefk.fields.CompositeForeignKey(null=True, null_if_equal=[], on_delete=django.db.models.deletion.DO_NOTHING, related_name='produto_desconto_origem_insercao', to='core.Tipo', to_fields={'codigo': compositefk.fields.LocalFieldValue('origem_insercao_codigo'), 'tipo': compositefk.fields.LocalFieldValue('origem_insercao_tipo')})),
            ],
            options={
                'db_table': 'produto_desconto',
                'abstract': False,
                'managed': True,
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='DescontoRelacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dat_insercao', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_edicao', models.DateTimeField(auto_now=True, null=True)),
                ('dat_delete', models.DateTimeField(null=True)),
                ('usr_insercao', models.IntegerField(null=True)),
                ('usr_edicao', models.IntegerField(null=True)),
                ('usr_delete', models.IntegerField(null=True)),
                ('origem_insercao_codigo', models.CharField(max_length=200, null=True)),
                ('origem_insercao_tipo', models.CharField(default='USR.ORIGEM', max_length=200, null=True)),
                ('origem_edicao_codigo', models.CharField(max_length=200, null=True)),
                ('origem_edicao_tipo', models.CharField(default='USR.ORIGEM', max_length=200, null=True)),
                ('origem_delete_codigo', models.CharField(max_length=200, null=True)),
                ('origem_delete_tipo', models.CharField(default='USR.ORIGEM', max_length=200, null=True)),
                ('status', models.BooleanField(default=True, null=True)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='produto.Categoria')),
                ('desconto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='produto.Desconto')),
                ('grupo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='produto.Grupo')),
                ('marca', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='produto.Marca')),
                ('origem_delete', compositefk.fields.CompositeForeignKey(null=True, null_if_equal=[], on_delete=django.db.models.deletion.DO_NOTHING, related_name='produto_descontorelacao_origem_delete', to='core.Tipo', to_fields={'codigo': compositefk.fields.LocalFieldValue('origem_delete_codigo'), 'tipo': compositefk.fields.LocalFieldValue('origem_delete_tipo')})),
                ('origem_edicao', compositefk.fields.CompositeForeignKey(null=True, null_if_equal=[], on_delete=django.db.models.deletion.DO_NOTHING, related_name='produto_descontorelacao_origem_edicao', to='core.Tipo', to_fields={'codigo': compositefk.fields.LocalFieldValue('origem_edicao_codigo'), 'tipo': compositefk.fields.LocalFieldValue('origem_edicao_tipo')})),
                ('origem_insercao', compositefk.fields.CompositeForeignKey(null=True, null_if_equal=[], on_delete=django.db.models.deletion.DO_NOTHING, related_name='produto_descontorelacao_origem_insercao', to='core.Tipo', to_fields={'codigo': compositefk.fields.LocalFieldValue('origem_insercao_codigo'), 'tipo': compositefk.fields.LocalFieldValue('origem_insercao_tipo')})),
                ('precolista', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='produto.PrecoLista')),
                ('produto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='produto.Produto')),
            ],
            options={
                'db_table': 'produto_descontorelacao',
                'abstract': False,
                'managed': True,
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ProdutoPreco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dat_insercao', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_edicao', models.DateTimeField(auto_now=True, null=True)),
                ('dat_delete', models.DateTimeField(null=True)),
                ('usr_insercao', models.IntegerField(null=True)),
                ('usr_edicao', models.IntegerField(null=True)),
                ('usr_delete', models.IntegerField(null=True)),
                ('origem_insercao_codigo', models.CharField(max_length=200, null=True)),
                ('origem_insercao_tipo', models.CharField(default='USR.ORIGEM', max_length=200, null=True)),
                ('origem_edicao_codigo', models.CharField(max_length=200, null=True)),
                ('origem_edicao_tipo', models.CharField(default='USR.ORIGEM', max_length=200, null=True)),
                ('origem_delete_codigo', models.CharField(max_length=200, null=True)),
                ('origem_delete_tipo', models.CharField(default='USR.ORIGEM', max_length=200, null=True)),
                ('status', models.BooleanField(default=True, null=True)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=14, null=True)),
                ('origem_delete', compositefk.fields.CompositeForeignKey(null=True, null_if_equal=[], on_delete=django.db.models.deletion.DO_NOTHING, related_name='produto_produtopreco_origem_delete', to='core.Tipo', to_fields={'codigo': compositefk.fields.LocalFieldValue('origem_delete_codigo'), 'tipo': compositefk.fields.LocalFieldValue('origem_delete_tipo')})),
                ('origem_edicao', compositefk.fields.CompositeForeignKey(null=True, null_if_equal=[], on_delete=django.db.models.deletion.DO_NOTHING, related_name='produto_produtopreco_origem_edicao', to='core.Tipo', to_fields={'codigo': compositefk.fields.LocalFieldValue('origem_edicao_codigo'), 'tipo': compositefk.fields.LocalFieldValue('origem_edicao_tipo')})),
                ('origem_insercao', compositefk.fields.CompositeForeignKey(null=True, null_if_equal=[], on_delete=django.db.models.deletion.DO_NOTHING, related_name='produto_produtopreco_origem_insercao', to='core.Tipo', to_fields={'codigo': compositefk.fields.LocalFieldValue('origem_insercao_codigo'), 'tipo': compositefk.fields.LocalFieldValue('origem_insercao_tipo')})),
                ('precolista', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='produto.PrecoLista')),
                ('produto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='produto.Produto')),
            ],
            options={
                'db_table': 'produto_preco',
                'abstract': False,
                'managed': True,
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='TipoDesconto',
            fields=[
                ('dat_insercao', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_edicao', models.DateTimeField(auto_now=True, null=True)),
                ('dat_delete', models.DateTimeField(null=True)),
                ('usr_insercao', models.IntegerField(null=True)),
                ('usr_edicao', models.IntegerField(null=True)),
                ('usr_delete', models.IntegerField(null=True)),
                ('origem_insercao_codigo', models.CharField(max_length=200, null=True)),
                ('origem_insercao_tipo', models.CharField(default='USR.ORIGEM', max_length=200, null=True)),
                ('origem_edicao_codigo', models.CharField(max_length=200, null=True)),
                ('origem_edicao_tipo', models.CharField(default='USR.ORIGEM', max_length=200, null=True)),
                ('origem_delete_codigo', models.CharField(max_length=200, null=True)),
                ('origem_delete_tipo', models.CharField(default='USR.ORIGEM', max_length=200, null=True)),
                ('status', models.BooleanField(default=True, null=True)),
                ('nome', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('descricao', models.CharField(max_length=200, null=True)),
                ('origem_delete', compositefk.fields.CompositeForeignKey(null=True, null_if_equal=[], on_delete=django.db.models.deletion.DO_NOTHING, related_name='produto_tipodesconto_origem_delete', to='core.Tipo', to_fields={'codigo': compositefk.fields.LocalFieldValue('origem_delete_codigo'), 'tipo': compositefk.fields.LocalFieldValue('origem_delete_tipo')})),
                ('origem_edicao', compositefk.fields.CompositeForeignKey(null=True, null_if_equal=[], on_delete=django.db.models.deletion.DO_NOTHING, related_name='produto_tipodesconto_origem_edicao', to='core.Tipo', to_fields={'codigo': compositefk.fields.LocalFieldValue('origem_edicao_codigo'), 'tipo': compositefk.fields.LocalFieldValue('origem_edicao_tipo')})),
                ('origem_insercao', compositefk.fields.CompositeForeignKey(null=True, null_if_equal=[], on_delete=django.db.models.deletion.DO_NOTHING, related_name='produto_tipodesconto_origem_insercao', to='core.Tipo', to_fields={'codigo': compositefk.fields.LocalFieldValue('origem_insercao_codigo'), 'tipo': compositefk.fields.LocalFieldValue('origem_insercao_tipo')})),
            ],
            options={
                'db_table': 'produto_tipodesconto',
                'abstract': False,
                'managed': True,
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='descontorelacao',
            name='produtopreco',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='produto.ProdutoPreco'),
        ),
        migrations.AddField(
            model_name='desconto',
            name='tipo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='produto.TipoDesconto'),
        ),
    ]
