from crypto_trader.sandbox.utils.db_tools import db_read, db_current_price


db_data = db_read("BTC")
print(db_current_price(db_data))

