# Generated by Django 3.1.2 on 2021-10-11 17:37

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import django_userforeignkey.models.fields
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sandbox', '0005_auto_20211011_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='coin_list',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('AAVE', 'Aave'), ('ANT', 'Aragon'), ('REP', 'Augur'), ('BAL', 'Balancer'), ('BTC', 'Bitcoin'), ('ADA', 'Cardano'), ('ATOM', 'Cosmos'), ('ETH', 'Ethereum'), ('ETC', 'EthereumClassic'), ('OXT', 'Orchid'), ('USDT', 'Tether'), ('XTZ', 'Tezos')], max_length=50),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='owner',
            field=django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mymodels', to=settings.AUTH_USER_MODEL, verbose_name='The user that is automatically assigned'),
        ),
    ]
