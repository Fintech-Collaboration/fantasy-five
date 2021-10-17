import pickle
import hvplot.pandas

import pandas as pd
import numpy  as np

from pathlib             import Path
from sklearn.ensemble    import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB

from sklearn.preprocessing  import StandardScaler
from pandas.tseries.offsets import DateOffset
from sklearn.metrics        import classification_report


data_path = r"C:\Users\JasonGarcia24\FINTECH\workspace\fantasy-five\crypto_trader\sandbox\data\aragon_5_year.csv"

# Import the OHLCV dataset into a Pandas Dataframe
ohlcv_df = pd.read_csv(
    Path(data_path), 
    index_col='ant_start_date', 
    infer_datetime_format=True, 
    parse_dates=True
)

# Review the DataFrame
ohlcv_df.head()

# Filter the date index and close columns
signals_df = ohlcv_df.loc[:, ["price_close"]]

# Use the pct_change function to generate  returns from close prices
signals_df["Actual Returns"] = signals_df["price_close"].pct_change()

# Drop all NaN values from the DataFrame
signals_df = signals_df.dropna()

# Set the short window and long window
short_window = 4
long_window = 100

# Generate the fast and slow simple moving averages (4 and 100 days, respectively)
signals_df['SMA_Fast'] = signals_df['price_close'].rolling(window=short_window).mean()
signals_df['SMA_Slow'] = signals_df['price_close'].rolling(window=long_window).mean()

signals_df = signals_df.dropna()

# Initialize the new Signal column
signals_df['Signal'] = 0.0

# When Actual Returns are greater than or equal to 0, generate signal to buy stock long
signals_df.loc[(signals_df['Actual Returns'] >= 0), 'Signal'] = 1

# When Actual Returns are less than 0, generate signal to sell stock short
signals_df.loc[(signals_df['Actual Returns'] < 0), 'Signal'] = -1

# Calculate the strategy returns and add them to the signals_df DataFrame
signals_df['Strategy Returns'] = signals_df['Actual Returns'] * signals_df['Signal'].shift()

# Assign a copy of the sma_fast and sma_slow columns to a features DataFrame called X
X = signals_df[['SMA_Fast', 'SMA_Slow']].shift().dropna()
y = signals_df['Signal']

# Select the start of the training period
training_begin = X.index.min()

# Select the ending period for the training data with an offset of 3 months
training_end = X.index.min() + DateOffset(months=3)

# Generate the X_train and y_train DataFrames
X_train = X.loc[training_begin:training_end]
y_train = y.loc[training_begin:training_end]

# Generate the X_test and y_test DataFrames
X_test = X.loc[training_end+DateOffset(hours=1):]
y_test = y.loc[training_end+DateOffset(hours=1):]

# Create a StandardScaler instance
scaler = StandardScaler()

# Apply the scaler model to fit the X-train data
X_scaler = scaler.fit(X_train)

# Transform the X_train and X_test DataFrames using the X_scaler
X_train_scaled = X_scaler.transform(X_train)
X_test_scaled = X_scaler.transform(X_test)

# Initiate the base estimator
base_estimator = GaussianNB()
base_estimator.fit(X_train_scaled, y_train)

# Initiate the model instance
boost_model = AdaBoostClassifier(
    base_estimator=base_estimator,
    n_estimators=20,
    learning_rate=2.6,
    random_state=1,
)
 
# Fit the model to the data using the training data
boost_model.fit(X_train_scaled, y_train)

with open(Path("./model_lowcap_boost.pkl"), "wb") as file:
               pickle.dump(boost_model, file)
 
"""
    Proof below
"""
# Use the testing data to make the model predictions
svm_pred = boost_model.predict(X_test_scaled)

# Review the model's predicted values
# YOUR CODE HERE
svm_pred_df = pd.DataFrame(svm_pred)
svm_pred_df.index = y_test.index
svm_pred_df.columns = ['Predicted']
svm_pred_df

# Use a classification report to evaluate the model using the predictions and testing data
svm_testing_report = classification_report(y_test, svm_pred)

# Print the classification report
# YOUR CODE HERE
print(svm_testing_report)

