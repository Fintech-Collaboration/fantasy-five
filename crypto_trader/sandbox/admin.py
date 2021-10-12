from django.contrib import admin
from sandbox.models import (
    Portfolio,
    Aave,
    Aragon,
    Augur,
    Balancer,
    Bitcoin,
    Cardano,
    Cosmos,
    Ethereum,
    EthereumClassic,
    Orchid,
    Tether,
    Tezos,
)


@admin.register(Aave)
class AaveAdmin(admin.ModelAdmin):
    pass


@admin.register(Aragon)
class AragonAdmin(admin.ModelAdmin):
    pass


@admin.register(Augur)
class AugurAdmin(admin.ModelAdmin):
    pass


@admin.register(Balancer)
class BalancerAdmin(admin.ModelAdmin):
    pass


@admin.register(Bitcoin)
class BitcoinAdmin(admin.ModelAdmin):
    pass


@admin.register(Cardano)
class CardanoAdmin(admin.ModelAdmin):
    pass


@admin.register(Cosmos)
class CosmosAdmin(admin.ModelAdmin):
    pass


@admin.register(Ethereum)
class EthereumAdmin(admin.ModelAdmin):
    pass


@admin.register(EthereumClassic)
class EthereumClassicAdmin(admin.ModelAdmin):
    pass


@admin.register(Orchid)
class OrchidAdmin(admin.ModelAdmin):
    pass


@admin.register(Tether)
class TetherAdmin(admin.ModelAdmin):
    pass


@admin.register(Tezos)
class TezosAdmin(admin.ModelAdmin):
    pass

admin.site.register(Portfolio)

