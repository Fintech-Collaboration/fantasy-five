# import pickle

# pkl_file = r"C:\Users\JasonGarcia24\FINTECH\workspace\fantasy-five\crypto_trader\sandbox\data\aave_model.pkl"

# with open(pkl_file, 'rb') as f:
#     data = pickle.load(f)

# breakpoint()

# gh = 1

from crypto_trader.sandbox.utils.ohlc_forecast import crypto_forecast

plt = crypto_forecast("price_close", "Bitcoin", "BTC")

breakpoint()
sl = 1
