import pickle
import hvplot.pandas
import functools

import pandas    as pd
import numpy     as np
import holoviews as hv

from fbprophet  import Prophet
from pathlib    import Path

from pandas.tseries.offsets import DateOffset
from sklearn.preprocessing  import StandardScaler
from sklearn.metrics        import classification_report

hv.extension('bokeh')


BASE_DIR  = Path(__file__).resolve().parent.parent
DATA_PATH = lambda n: f"{BASE_DIR}/data/{n.lower()}_5_year.csv"


def set__str__ (_str):
    def wrapper (f):
        class FuncType:
            def __call__ (self, *args, **kwargs):
                # call the original function
                return f(*args, **kwargs)
            def __str__ (self):
                # call the custom __str__ function
                return _str

        # decorate with functool.wraps to make the resulting function appear like f
        return functools.wraps(f)(FuncType())
    return wrapper


def dmac(df, short=50, long=100):
    df["SMA_short"] = df["price_close"].rolling(window=short).mean()
    df["SMA_long"]  = df["price_close"].rolling(window=long ).mean()
    df["signal"]    = 0.0

    df["signal"][short:] = np.where(
        df["SMA_short"][short:] > df["SMA_long"][short:], 1.0, 0.0
    )

    df["entry_exit"] = df["signal"].diff()

    return df


def ohlc_forecast(name="Bitcoin", ticker="BTC", col="price_close"):
    """
    sr_ucb_project02_prophet_cryptoforecast_aave.ipynb

    Automatically generated by Colaboratory.

    Original file is located at
    https://colab.research.google.com/drive/1zJIeUQdU7XG1wSND6siFX6xQ54C6FyV1

    # UCB PROJECT 02: Forecasting Crypto

    ## Install and import the required libraries and dependencies
    """

    TITLE_DICT = {
        "price_close": "Market Open",
        "price_high":  "Daily High",
        "price_low":   "Daily Low",
        "price_close": "Market Close",
    }

    name   = name.lower()
    ticker = ticker.lower()

    # Variables
    data_path        = DATA_PATH(name)
    forecast_period  = 90
    index_column     = ticker + "_start_date"
    x_val            = ticker + "_start_date.year"
    y_val            = ticker + "_start_date.quarter"
    title_heatmap = f"Transaction Volume Heatmap For: {TITLE_DICT[col]}"

    # Set the "Date" column as the Datetime Index.
    df_crypto = pd.read_csv(
    data_path, 
    index_col=index_column, 
    parse_dates = True, 
    infer_datetime_format = True
    )

    # Reserve a DF with no Index, if needed
    df_crypto_noIndex = df_crypto.reset_index()
    df_crypto_noIndex.head()

    # Separate out the coulmns that you are interested in ... 
    df_crypto_index = df_crypto[[col]]

    # Do we have any nulls?
    df_crypto_index.isnull().sum()

    """ ANALYSIS """
    # Price Trends
    df_crypto_index.plot(
        figsize=(20,10),
        xlabel="Date",
        ylabel=" ".join([s.capitalize() for s in f"{col}".split(" ")]),
        title=f"{TITLE_DICT[col].split(' ')[0]} Price Trend"
    )

    # HeatMap for Crypto
    hv.extension('bokeh')

    heat_plt = df_crypto_index.hvplot.heatmap(
        x=x_val,
        y=y_val,
        C=col,
        cmap = "Purples",
        xlabel="Year",
        ylabel="Year by Quarter",
        title=title_heatmap,
        width=1000,
        height=500
    ).aggregate(
        function=np.mean
    )

    """ FORECAST """
    # Prep the data
    df_crypto_noindex_prophet = df_crypto_index.reset_index()

    # rename the columnas as part of the prep-work
    df_crypto_noindex_prophet.columns = ['ds', 'y']

    # Are there any nulls?
    df_crypto_noindex_prophet = df_crypto_noindex_prophet.dropna()

    # Remove Time Zone
    df_crypto_noindex_prophet['ds'] = df_crypto_noindex_prophet['ds'].dt.tz_localize(None)

    # Create the Model
    m_crypto = Prophet()

    # Fit Model
    m_crypto.fit(df_crypto_noindex_prophet)

    # Setup Predictions
    future_crypto = m_crypto.make_future_dataframe(periods=forecast_period, freq='D')

    # Make Predictions
    forecast_crypto = m_crypto.predict(future_crypto)

    # plot the forecast
    hv.extension('bokeh')
    plt = m_crypto.plot(
        forecast_crypto,
        xlabel="Time Line - (ds)",
        ylabel=f"Prediction: {TITLE_DICT[col]} - (y)",
        figsize=(16,8),
    )

    """ ACTUAL price prediction for the Forecast range (set in variable declaration) ... in case we want to show """
    forecast_crypto[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(forecast_period)

    return forecast_crypto, df_crypto_noindex_prophet


@set__str__("svc")
def ml_svc_apply(model: str, name: str, ticker: str, market_cap="midcap"):
    data_path  = DATA_PATH(name)
    model_path = f"{BASE_DIR}/ml_resources/model_{market_cap.lower()}_svc.pkl"
    
    forecast = pd.read_pickle(model_path)
    ohlcv_df = pd.read_csv(
        data_path,
        index_col=f"{ticker.lower()}_start_date",
        infer_datetime_format=True,
        parse_dates=True,
    ).sort_index().drop_duplicates()

    # Filter the date index and close columns
    signals_df = ohlcv_df.loc[:, ["price_close"]]

    # Use the pct_change function to generate  returns from close prices
    signals_df["Actual Returns"] = signals_df["price_close"].pct_change()

    # Drop all NaN values from the DataFrame
    signals_df = signals_df.dropna()

    # Set the short window and long window
    short_window = 4
    long_window  = 100

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

    scaler = StandardScaler()

    X_scaler = scaler.fit(X)
    X_scaled = X_scaler.transform(X)

    pred    = forecast.predict(X_scaled)
    pred_df = pd.DataFrame(pred)
    pred_df.index   = y.index[1:]
    pred_df.columns = ["Predicted"]

    # Use a classification report to evaluate the model using the predictions and testing data
    svm_testing_report = classification_report(y[1:], pred)

    # Print the classification report
    print(svm_testing_report)

    # Create a predictions DataFrame
    predictions_df = pd.DataFrame(index=X.index)

    # Add the SVM model predictions to the DataFrame
    predictions_df['Predicted'] = pred

    # Add the actual returns to the DataFrame
    predictions_df['Actual Returns'] = signals_df['Actual Returns'][1:]

    # Add the strategy returns to the DataFrame
    predictions_df['Strategy Returns'] = predictions_df['Actual Returns'] * predictions_df['Predicted']

    return predictions_df


@set__str__("adaboost")
def ml_adaboost_apply(model: str, name: str, ticker: str):
    data_path  = DATA_PATH(name)
    model_path = f"{BASE_DIR}/ml_resources/{ticker.lower()}_{model.lower()}_model.pkl"
    
    svm_model = pd.read_pickle(model_path)
    ohlcv_df  = pd.read_csv(
        data_path,
        index_col=f"{ticker.lower()}_start_date",
        infer_datetime_format=True,
        parse_dates=True,
    ).sort_index().drop_duplicates()

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

    # Create the target set selecting the Signal column and assiging it to y
    y = signals_df['Signal']

    # Select the start of the training period
    training_begin = X.index.min()

    # Select the ending period for the training data with an offset of 3 months
    training_end = X.index.min() + DateOffset(months=3)

    # Generate the X_train and y_train DataFrames
    X_train = X.loc[training_begin:training_end]
    y_train = y.loc[training_begin:training_end]

    # Generate the X_test and y_test DataFrames
    X_test = X.loc[training_end+DateOffset(days=1):]
    y_test = y.loc[training_end+DateOffset(days=1):]

    # Scale the features DataFrames

    # Create a StandardScaler instance
    scaler = StandardScaler()

    # Apply the scaler model to fit the X-train data
    X_scaler = scaler.fit(X_train)

    # Transform the X_train and X_test DataFrames using the X_scaler
    X_train_scaled = X_scaler.transform(X_train)
    X_test_scaled = X_scaler.transform(X_test)

    # Use the testing data to make the model predictions
    svm_pred = svm_model.predict(X_test_scaled)

    # Review the model's predicted values
    svm_pred_df = pd.DataFrame(svm_pred)
    svm_pred_df.index = y_test.index
    svm_pred_df.columns = ['Predicted']
    svm_pred_df

    # Use a classification report to evaluate the model using the predictions and testing data
    svm_testing_report = classification_report(y_test, svm_pred)

    # Print the classification report
    print(svm_testing_report)

    # Create a predictions DataFrame
    predictions_df = pd.DataFrame(index=X_test.index)

    # Add the SVM model predictions to the DataFrame
    predictions_df['Predicted'] = svm_pred

    # Add the actual returns to the DataFrame
    predictions_df = pd.concat(
        [predictions_df, signals_df[['Actual Returns']]],
        axis=1,
        join="inner",
    )

    # Add the strategy returns to the DataFrame
    predictions_df['Strategy Returns'] = predictions_df['Actual Returns'] * predictions_df['Predicted']

    return predictions_df


@set__str__("adaboost0")
def ml_adaboost_apply0(model: str, name: str, ticker: str):
    data_path  = DATA_PATH(name)
    model_path = f"{BASE_DIR}/ml_resources/{ticker.lower()}_{model.lower()}_model.pkl"
    
    forecast = pd.read_pickle(model_path)
    ohlcv_df = pd.read_csv(
        data_path,
        index_col=f"{ticker.lower()}_start_date",
        infer_datetime_format=True,
        parse_dates=True,
    ).sort_index().drop_duplicates()

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
    X_test = X.loc[training_end+DateOffset(days=1):]
    y_test = y.loc[training_end+DateOffset(days=1):]

    # Create a StandardScaler instance
    scaler = StandardScaler()

    # Apply the scaler model to fit the X-train data
    X_scaler = scaler.fit(X)

    # Transform the X_train and X_test DataFrames using the X_scaler
    X_test_scaled = X_scaler.transform(X_test)

    pred    = forecast.predict(X_test_scaled)
    pred_df = pd.DataFrame(pred)
    pred_df.index   = y_test.index
    pred_df.columns = ["Predicted"]

    # Use a classification report to evaluate the model using the predictions and testing data
    svm_testing_report = classification_report(y_test, pred)

    # Print the classification report
    print(svm_testing_report)

    # Create a predictions DataFrame
    predictions_df = pd.DataFrame(index=X_test.index)
    
    # Add the SVM model predictions to the DataFrame
    predictions_df['Predicted'] = pred

    # Add the SVM model predictions to the DataFrame
    predictions_df = pd.concat(
        [predictions_df, signals_df[['Actual Returns']]],
        axis=1,
        join="inner",
    )

    # Add the strategy returns to the DataFrame
    predictions_df['Strategy Returns'] = predictions_df['Actual Returns'] * predictions_df['Predicted']

    return predictions_df

