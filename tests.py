from crypto_trader.sandbox.utils.algo_trading import ml_cluster_apply


names   = ['aave', 'aragon', 'augur', 'balancer', 'bitcoin', 'cardano', 'cosmos', 'ethereum', 'ethereumclassic', 'orchid', 'tether', 'tezos']
tickers = ['aave', 'ant', 'rep', 'bal', 'btc', 'ada', 'atom', 'eth', 'etc', 'oxt', 'usdt', 'xtz']


pca_df = ml_cluster_apply(names, tickers)

breakpoint()

gh = 1

