import pickle
import hvplot.pandas
import functools

import pandas    as pd
import numpy     as np
import holoviews as hv

from fbprophet  import Prophet
from pathlib    import Path

from sklearn.cluster        import KMeans
from sklearn.decomposition  import PCA
from sklearn.preprocessing  import StandardScaler
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


def ohlc_forecast(df_crypto, col="price_close"):
    """
    sr_ucb_project02_prophet_cryptoforecast_aave.ipynb

    Automatically generated by Colaboratory.

    Original file is located at
    https://colab.research.google.com/drive/1zJIeUQdU7XG1wSND6siFX6xQ54C6FyV1

    # UCB PROJECT 02: Forecasting Crypto

    ## Install and import the required libraries and dependencies
    """

    # Variables
    forecast_period  = 90

    # Reserve a DF with no Index, if needed
    df_crypto_noIndex = df_crypto.reset_index()
    df_crypto_noIndex.head()

    # Separate out the coulmns that you are interested in ... 
    df_crypto_index = df_crypto[[col]]

    # Do we have any nulls?
    df_crypto_index.isnull().sum()

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

    """ ACTUAL price prediction for the Forecast range (set in variable declaration) ... in case we want to show """
    forecast_crypto[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(forecast_period)

    return forecast_crypto


@set__str__("svc")
def ml_svc_apply(ohlcv_df: pd.DataFrame, market_cap="midcap"):
    model_path = f"{BASE_DIR}/ml_resources/model_{market_cap.lower()}_svc.pkl"
    
    forecast = pd.read_pickle(model_path)

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
def ml_adaboost_apply(ohlcv_df: pd.DataFrame, ticker: str):
    model_path = f"{BASE_DIR}/ml_resources/{ticker.lower()}_adaboost_model.pkl"
    
    svm_model = pd.read_pickle(model_path)

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


def ml_cluster_apply(names: str, tickers: str):
    df_market_data = pd.DataFrame()

    for name, ticker in zip(names, tickers):
        data_path = DATA_PATH(name)
        crypto_df = pd.read_csv(
            data_path,
            index_col=f"{ticker}_start_date"
        ).sort_index().drop_duplicates()

        price_changes = dict()
        price_changes['coin_id'] = name

        for y in [2, 7, 14, 30, 60, 200]:
            k = 'price_change_pct' + str(y) + 'd'
            price_changes[k] = [crypto_df.rolling(window=int(y)).mean().pct_change().mean()['price_close']]

        temp_df        = pd.DataFrame(price_changes)
        df_market_data = pd.concat([temp_df, df_market_data]).reset_index(drop=True)

    df_market_data = df_market_data.set_index('coin_id').dropna()

    # Use the `StandardScaler()` module from scikit-learn to normalize the data from the CSV file
    scaled_data = StandardScaler().fit_transform(df_market_data)

    # Create a DataFrame with the scaled data
    df_market_data_scaled = pd.DataFrame(
        scaled_data,
        columns=df_market_data.columns
    )

    # Copy the crypto names from the original data
    df_market_data_scaled["coin_id"] = df_market_data.index

    # Set the coinid column as index
    df_market_data_scaled = df_market_data_scaled.set_index("coin_id")

    # Create a list with the number of k-values to try
    # Use a range from 1 to 11
    k = range(1,11)

    # Create an empy list to store the inertia values
    inertia = []

    # Create a for loop to compute the inertia with each possible value of k
    for i in k:
        model = KMeans(n_clusters=i, random_state=1)
        model.fit(df_market_data_scaled)
        inertia.append(model.inertia_)

    # Initialize the K-Means model using the best value for k
    model = KMeans(n_clusters=4, random_state=1)

    # Fit the K-Means model using the scaled data
    model.fit(df_market_data_scaled)

    # Predict the clusters to group the cryptocurrencies using the scaled data
    k4 = model.predict(df_market_data_scaled)

    # Add a new column to the DataFrame with the predicted clusters
    df_market_data_scaled['predicted_clusters'] = k4

    # Create a PCA model instance and set `n_components=3`.
    pca = PCA(n_components=3)

    # Use the PCA model with `fit_transform` to reduce to 
    # three principal components.
    pca_fit = pca.fit_transform(df_market_data_scaled)

    # Creating a DataFrame with the PCA data
    pca_fit_df = pd.DataFrame(pca_fit, columns=["PCA1", "PCA2", "PCA3"])

    # Copy the crypto names from the original data
    pca_fit_df['coin_id'] = df_market_data.index

    # Set the coinid column as index
    pca_fit_df.set_index('coin_id', inplace=True)

    # Create a list with the number of k-values to try
    # Use a range from 1 to 11
    k = range(1, 11)

    # Create an empy list to store the inertia values
    inertia = []

    # Create a for loop to compute the inertia with each possible value of k
    for i in k:
        pca_model = KMeans(n_clusters=i, random_state=1)
        pca_model.fit(pca_fit_df)
        inertia.append(pca_model.inertia_)

    # Create a dictionary with the data to plot the Elbow curve
    pca_elbow_dict = {"k":k, "inertia":inertia}

    # Create a DataFrame with the data to plot the Elbow curve
    pca_elbow_df = pd.DataFrame(pca_elbow_dict)

    # Initialize the K-Means model using the best value for k
    elbow_model = KMeans(n_clusters=4, random_state=1)

    # Fit the K-Means model using the PCA data
    elbow_model.fit(pca_fit_df)

    # Predict the clusters to group the cryptocurrencies using the PCA data
    pca_k4 = elbow_model.predict(pca_fit_df)

    # Add a new column to the DataFrame with the predicted clusters
    pca_fit_df['predicted_clusters'] = pca_k4

    return pca_fit_df

