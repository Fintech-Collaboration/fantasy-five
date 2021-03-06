# Generated by Django 3.1.2 on 2021-10-12 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('sandbox', '0013_auto_20211012_1904'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('price_open', models.FloatField(default=0.0)),
                ('price_high', models.FloatField(default=0.0)),
                ('price_low', models.FloatField(default=0.0)),
                ('price_close', models.FloatField(default=0.0)),
                ('volume_traded', models.FloatField(default=0.0)),
                ('trades_count', models.IntegerField(default=0)),
                ('ticker', models.CharField(max_length=8)),
                ('name', models.CharField(max_length=30)),
                ('count', models.FloatField(default=0.0)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_sandbox.coin_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.AlterModelOptions(
            name='aave',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='aragon',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='augur',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='balancer',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='bitcoin',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='cardano',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='cosmos',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='ethereum',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='ethereumclassic',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='orchid',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='tether',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='tezos',
            options={'base_manager_name': 'objects'},
        ),
        migrations.RemoveField(
            model_name='aave',
            name='count',
        ),
        migrations.RemoveField(
            model_name='aave',
            name='id',
        ),
        migrations.RemoveField(
            model_name='aave',
            name='name',
        ),
        migrations.RemoveField(
            model_name='aave',
            name='portfolio',
        ),
        migrations.RemoveField(
            model_name='aave',
            name='price_close',
        ),
        migrations.RemoveField(
            model_name='aave',
            name='price_high',
        ),
        migrations.RemoveField(
            model_name='aave',
            name='price_low',
        ),
        migrations.RemoveField(
            model_name='aave',
            name='price_open',
        ),
        migrations.RemoveField(
            model_name='aave',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='aave',
            name='ticker',
        ),
        migrations.RemoveField(
            model_name='aave',
            name='trades_count',
        ),
        migrations.RemoveField(
            model_name='aave',
            name='volume_traded',
        ),
        migrations.RemoveField(
            model_name='aragon',
            name='count',
        ),
        migrations.RemoveField(
            model_name='aragon',
            name='id',
        ),
        migrations.RemoveField(
            model_name='aragon',
            name='name',
        ),
        migrations.RemoveField(
            model_name='aragon',
            name='portfolio',
        ),
        migrations.RemoveField(
            model_name='aragon',
            name='price_close',
        ),
        migrations.RemoveField(
            model_name='aragon',
            name='price_high',
        ),
        migrations.RemoveField(
            model_name='aragon',
            name='price_low',
        ),
        migrations.RemoveField(
            model_name='aragon',
            name='price_open',
        ),
        migrations.RemoveField(
            model_name='aragon',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='aragon',
            name='ticker',
        ),
        migrations.RemoveField(
            model_name='aragon',
            name='trades_count',
        ),
        migrations.RemoveField(
            model_name='aragon',
            name='volume_traded',
        ),
        migrations.RemoveField(
            model_name='augur',
            name='count',
        ),
        migrations.RemoveField(
            model_name='augur',
            name='id',
        ),
        migrations.RemoveField(
            model_name='augur',
            name='name',
        ),
        migrations.RemoveField(
            model_name='augur',
            name='portfolio',
        ),
        migrations.RemoveField(
            model_name='augur',
            name='price_close',
        ),
        migrations.RemoveField(
            model_name='augur',
            name='price_high',
        ),
        migrations.RemoveField(
            model_name='augur',
            name='price_low',
        ),
        migrations.RemoveField(
            model_name='augur',
            name='price_open',
        ),
        migrations.RemoveField(
            model_name='augur',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='augur',
            name='ticker',
        ),
        migrations.RemoveField(
            model_name='augur',
            name='trades_count',
        ),
        migrations.RemoveField(
            model_name='augur',
            name='volume_traded',
        ),
        migrations.RemoveField(
            model_name='balancer',
            name='count',
        ),
        migrations.RemoveField(
            model_name='balancer',
            name='id',
        ),
        migrations.RemoveField(
            model_name='balancer',
            name='name',
        ),
        migrations.RemoveField(
            model_name='balancer',
            name='portfolio',
        ),
        migrations.RemoveField(
            model_name='balancer',
            name='price_close',
        ),
        migrations.RemoveField(
            model_name='balancer',
            name='price_high',
        ),
        migrations.RemoveField(
            model_name='balancer',
            name='price_low',
        ),
        migrations.RemoveField(
            model_name='balancer',
            name='price_open',
        ),
        migrations.RemoveField(
            model_name='balancer',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='balancer',
            name='ticker',
        ),
        migrations.RemoveField(
            model_name='balancer',
            name='trades_count',
        ),
        migrations.RemoveField(
            model_name='balancer',
            name='volume_traded',
        ),
        migrations.RemoveField(
            model_name='bitcoin',
            name='count',
        ),
        migrations.RemoveField(
            model_name='bitcoin',
            name='id',
        ),
        migrations.RemoveField(
            model_name='bitcoin',
            name='name',
        ),
        migrations.RemoveField(
            model_name='bitcoin',
            name='portfolio',
        ),
        migrations.RemoveField(
            model_name='bitcoin',
            name='price_close',
        ),
        migrations.RemoveField(
            model_name='bitcoin',
            name='price_high',
        ),
        migrations.RemoveField(
            model_name='bitcoin',
            name='price_low',
        ),
        migrations.RemoveField(
            model_name='bitcoin',
            name='price_open',
        ),
        migrations.RemoveField(
            model_name='bitcoin',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='bitcoin',
            name='ticker',
        ),
        migrations.RemoveField(
            model_name='bitcoin',
            name='trades_count',
        ),
        migrations.RemoveField(
            model_name='bitcoin',
            name='volume_traded',
        ),
        migrations.RemoveField(
            model_name='cardano',
            name='count',
        ),
        migrations.RemoveField(
            model_name='cardano',
            name='id',
        ),
        migrations.RemoveField(
            model_name='cardano',
            name='name',
        ),
        migrations.RemoveField(
            model_name='cardano',
            name='portfolio',
        ),
        migrations.RemoveField(
            model_name='cardano',
            name='price_close',
        ),
        migrations.RemoveField(
            model_name='cardano',
            name='price_high',
        ),
        migrations.RemoveField(
            model_name='cardano',
            name='price_low',
        ),
        migrations.RemoveField(
            model_name='cardano',
            name='price_open',
        ),
        migrations.RemoveField(
            model_name='cardano',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='cardano',
            name='ticker',
        ),
        migrations.RemoveField(
            model_name='cardano',
            name='trades_count',
        ),
        migrations.RemoveField(
            model_name='cardano',
            name='volume_traded',
        ),
        migrations.RemoveField(
            model_name='cosmos',
            name='count',
        ),
        migrations.RemoveField(
            model_name='cosmos',
            name='id',
        ),
        migrations.RemoveField(
            model_name='cosmos',
            name='name',
        ),
        migrations.RemoveField(
            model_name='cosmos',
            name='portfolio',
        ),
        migrations.RemoveField(
            model_name='cosmos',
            name='price_close',
        ),
        migrations.RemoveField(
            model_name='cosmos',
            name='price_high',
        ),
        migrations.RemoveField(
            model_name='cosmos',
            name='price_low',
        ),
        migrations.RemoveField(
            model_name='cosmos',
            name='price_open',
        ),
        migrations.RemoveField(
            model_name='cosmos',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='cosmos',
            name='ticker',
        ),
        migrations.RemoveField(
            model_name='cosmos',
            name='trades_count',
        ),
        migrations.RemoveField(
            model_name='cosmos',
            name='volume_traded',
        ),
        migrations.RemoveField(
            model_name='ethereum',
            name='count',
        ),
        migrations.RemoveField(
            model_name='ethereum',
            name='id',
        ),
        migrations.RemoveField(
            model_name='ethereum',
            name='name',
        ),
        migrations.RemoveField(
            model_name='ethereum',
            name='portfolio',
        ),
        migrations.RemoveField(
            model_name='ethereum',
            name='price_close',
        ),
        migrations.RemoveField(
            model_name='ethereum',
            name='price_high',
        ),
        migrations.RemoveField(
            model_name='ethereum',
            name='price_low',
        ),
        migrations.RemoveField(
            model_name='ethereum',
            name='price_open',
        ),
        migrations.RemoveField(
            model_name='ethereum',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='ethereum',
            name='ticker',
        ),
        migrations.RemoveField(
            model_name='ethereum',
            name='trades_count',
        ),
        migrations.RemoveField(
            model_name='ethereum',
            name='volume_traded',
        ),
        migrations.RemoveField(
            model_name='ethereumclassic',
            name='count',
        ),
        migrations.RemoveField(
            model_name='ethereumclassic',
            name='id',
        ),
        migrations.RemoveField(
            model_name='ethereumclassic',
            name='name',
        ),
        migrations.RemoveField(
            model_name='ethereumclassic',
            name='portfolio',
        ),
        migrations.RemoveField(
            model_name='ethereumclassic',
            name='price_close',
        ),
        migrations.RemoveField(
            model_name='ethereumclassic',
            name='price_high',
        ),
        migrations.RemoveField(
            model_name='ethereumclassic',
            name='price_low',
        ),
        migrations.RemoveField(
            model_name='ethereumclassic',
            name='price_open',
        ),
        migrations.RemoveField(
            model_name='ethereumclassic',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='ethereumclassic',
            name='ticker',
        ),
        migrations.RemoveField(
            model_name='ethereumclassic',
            name='trades_count',
        ),
        migrations.RemoveField(
            model_name='ethereumclassic',
            name='volume_traded',
        ),
        migrations.RemoveField(
            model_name='orchid',
            name='count',
        ),
        migrations.RemoveField(
            model_name='orchid',
            name='id',
        ),
        migrations.RemoveField(
            model_name='orchid',
            name='name',
        ),
        migrations.RemoveField(
            model_name='orchid',
            name='portfolio',
        ),
        migrations.RemoveField(
            model_name='orchid',
            name='price_close',
        ),
        migrations.RemoveField(
            model_name='orchid',
            name='price_high',
        ),
        migrations.RemoveField(
            model_name='orchid',
            name='price_low',
        ),
        migrations.RemoveField(
            model_name='orchid',
            name='price_open',
        ),
        migrations.RemoveField(
            model_name='orchid',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='orchid',
            name='ticker',
        ),
        migrations.RemoveField(
            model_name='orchid',
            name='trades_count',
        ),
        migrations.RemoveField(
            model_name='orchid',
            name='volume_traded',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='coin_list',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='investment',
        ),
        migrations.RemoveField(
            model_name='tether',
            name='count',
        ),
        migrations.RemoveField(
            model_name='tether',
            name='id',
        ),
        migrations.RemoveField(
            model_name='tether',
            name='name',
        ),
        migrations.RemoveField(
            model_name='tether',
            name='portfolio',
        ),
        migrations.RemoveField(
            model_name='tether',
            name='price_close',
        ),
        migrations.RemoveField(
            model_name='tether',
            name='price_high',
        ),
        migrations.RemoveField(
            model_name='tether',
            name='price_low',
        ),
        migrations.RemoveField(
            model_name='tether',
            name='price_open',
        ),
        migrations.RemoveField(
            model_name='tether',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='tether',
            name='ticker',
        ),
        migrations.RemoveField(
            model_name='tether',
            name='trades_count',
        ),
        migrations.RemoveField(
            model_name='tether',
            name='volume_traded',
        ),
        migrations.RemoveField(
            model_name='tezos',
            name='count',
        ),
        migrations.RemoveField(
            model_name='tezos',
            name='id',
        ),
        migrations.RemoveField(
            model_name='tezos',
            name='name',
        ),
        migrations.RemoveField(
            model_name='tezos',
            name='portfolio',
        ),
        migrations.RemoveField(
            model_name='tezos',
            name='price_close',
        ),
        migrations.RemoveField(
            model_name='tezos',
            name='price_high',
        ),
        migrations.RemoveField(
            model_name='tezos',
            name='price_low',
        ),
        migrations.RemoveField(
            model_name='tezos',
            name='price_open',
        ),
        migrations.RemoveField(
            model_name='tezos',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='tezos',
            name='ticker',
        ),
        migrations.RemoveField(
            model_name='tezos',
            name='trades_count',
        ),
        migrations.RemoveField(
            model_name='tezos',
            name='volume_traded',
        ),
        migrations.AddField(
            model_name='portfolio',
            name='balance',
            field=models.FloatField(default=0.0),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_executed', models.DateTimeField()),
                ('coin_count', models.FloatField(default=0.0)),
                ('coin_cost', models.FloatField(default=0.0)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sandbox.coin')),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sandbox.portfolio')),
            ],
        ),
        migrations.AddField(
            model_name='aave',
            name='coin_ptr',
            field=models.OneToOneField(auto_created=True, default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sandbox.coin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aragon',
            name='coin_ptr',
            field=models.OneToOneField(auto_created=True, default=-1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sandbox.coin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='augur',
            name='coin_ptr',
            field=models.OneToOneField(auto_created=True, default=-2, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sandbox.coin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='balancer',
            name='coin_ptr',
            field=models.OneToOneField(auto_created=True, default=-3, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sandbox.coin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bitcoin',
            name='coin_ptr',
            field=models.OneToOneField(auto_created=True, default=-4, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sandbox.coin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cardano',
            name='coin_ptr',
            field=models.OneToOneField(auto_created=True, default=-5, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sandbox.coin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cosmos',
            name='coin_ptr',
            field=models.OneToOneField(auto_created=True, default=-6, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sandbox.coin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ethereum',
            name='coin_ptr',
            field=models.OneToOneField(auto_created=True, default=-7, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sandbox.coin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ethereumclassic',
            name='coin_ptr',
            field=models.OneToOneField(auto_created=True, default=-8, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sandbox.coin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orchid',
            name='coin_ptr',
            field=models.OneToOneField(auto_created=True, default=-9, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sandbox.coin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='portfolio',
            name='coins',
            field=models.ManyToManyField(through='sandbox.Transaction', to='sandbox.Coin'),
        ),
        migrations.AddField(
            model_name='tether',
            name='coin_ptr',
            field=models.OneToOneField(auto_created=True, default=-10, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sandbox.coin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tezos',
            name='coin_ptr',
            field=models.OneToOneField(auto_created=True, default=-11, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sandbox.coin'),
            preserve_default=False,
        ),
    ]
