# import pickle

# pkl_file = r"C:\Users\JasonGarcia24\FINTECH\workspace\fantasy-five\crypto_trader\sandbox\data\aave_model.pkl"

# with open(pkl_file, 'rb') as f:
#     data = pickle.load(f)

# breakpoint()

# gh = 1

import pickle
from crypto_trader.sandbox.utils.algo_trading import ohlc_forecast, ml_apply

pickle_path = r"C:\Users\JasonGarcia24\FINTECH\workspace\fantasy-five\crypto_trader\sandbox\data\aave_model.pkl"
forecast_df = ml_apply(pickle_path)

breakpoint()
sl = 1
