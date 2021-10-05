import pandas as pd

from pathlib           import Path
from django.shortcuts  import render
from plotly.offline    import plot
from plotly.graph_objs import Scatter


TEST_DATA = r"C:\Users\JasonGarcia24\FINTECH\workspace\fantasy-five\data\latest-quotes_data_ALL.csv"


def home(request):
    df = pd.read_csv(
        Path(TEST_DATA),
        index_col="last_updated",
        parse_dates=True,
        infer_datetime_format=True,
    )

    df_btc = df.loc[df["symbol"]=="BTC"]
    x_data = df_btc.index
    y_data = df_btc["quote.USD.price"]

    plot_div = plot([Scatter(
        x=x_data,
        y=y_data,
        mode='lines',
        name='BTC',
        opacity=0.8,
        marker_color='green',
    )],
    output_type='div')    

    context = {"plot_div": plot_div}
    return render(request, "sandbox/home.html", context=context)



# def home(request):
#     x_data = [0,1,2,3]
#     y_data = [x**2 for x in x_data]
#     plot_div = plot([Scatter(x=x_data, y=y_data,
#                         mode='lines', name='test',
#                         opacity=0.8, marker_color='green')],
#                output_type='div')

#     context = {"plot_div": plot_div}
#     return render(request, "sandbox/home.html", context=context)

