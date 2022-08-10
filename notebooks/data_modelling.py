import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from pandas import read_csv

from sklearn.metrics import mean_squared_error
import dateutil.parser # for handling the conversion of datetime formats
from datetime import timedelta # for operating the datetime objects
from statsmodels.tsa. statespace.sarimax import SARIMAX

import warnings
warnings.filterwarnings('ignore')

url = '../processed_data/output.csv'
df = pd.read_csv(url, index_col = 'year', parse_dates=True, infer_datetime_format=True)
df = df.sort_index(axis=0, level=None, ascending=True, inplace=False, kind='quicksort', na_position='last', sort_remaining=True, ignore_index=False, key=None)
countries=df['country'].unique()
# Add a attribute name to add it in the prediction/forecasting
columns = ['sucid_in_hundredk','gdp_per_capita', 'lifeexpectancy','population']

for i, country in enumerate(countries):
    print("Creating a time series for country ",country," with parameter ", columns)
    country_df = df[(df.country == country)]
    country_with_columns = pd.DataFrame(country_df, columns=columns)
    # adding all deaths together and group by year
    country_with_columns = country_with_columns.groupby(['year'])[columns].transform('sum')
    #country_with_columns = pd.Series.to_frame(country_with_columns)
    country_with_columns['year'] = list(country_with_columns.index)
    country_with_columns = country_with_columns.drop_duplicates()
    country_with_columns = country_with_columns.drop(labels='year', axis=1)

    country_with_columns.to_csv('../processed_data/country_wise/data/'+str(country)+'.csv')

print("All files are written in the directory.")
print("\n"*5)


# evaluate an SARIMA model for a given order (p,d,q)
def evaluate_sarima_model(X, sarima_order):

    # prepare training dataset
    train_size = int(len(X) * 0.66)
    train, test = X[0:train_size], X[train_size:]
    history = [x for x in train]

    # make predictions
    predictions = list()

    for t in range(len(test)):
        model = SARIMAX(history, order=sarima_order)
        model_fit = model.fit(disp=0)
        yhat = model_fit.forecast()[0]
        predictions.append(yhat)
        history.append(test[t])

    # calculate out of sample error
    rmse = sqrt(mean_squared_error(test, predictions))

    return rmse

# evaluate combinations of p, d and q values for an SARIMA model - Grid Search
def evaluate_models(dataset, p_values, d_values, q_values):
    
    dataset = dataset.astype('float32')
    best_score, best_cfg = float("inf"), None

    for p in p_values:

        for d in d_values:

            for q in q_values:

                order = (p,d,q)
                try:
                    rmse = evaluate_sarima_model(dataset, order)
                    if rmse < best_score:
                        best_score, best_cfg = rmse, order
                    #print('SARIMA%s RMSE=%.3f' % (order,rmse))
                except:
                    continue

        #print('Best SARIMA%s RMSE=%.3f' % (best_cfg, best_score))

    print('Best SARIMA%s RMSE=%.3f' % (best_cfg, best_score))
    return best_cfg, best_score


# function to check if the year is leap year or not
def is_leap_year(year):

    if (year%4) == 0:
        if (year%100) == 0:
            if (year%400) == 0:
                return True
            else:
                return False
        else:
             return True
    else:
        return False

def forecasted_series_to_df(series, forecasted_series_, npast_year, name_of_forecasted_column, name_of_datetime_index_column):
  forecasted_series = forecasted_series_.copy()
  y = 0
  index_for_forcaste = []
  index_for_forcaste.append(series.index[-npast_year-1])
  for i in range(len(forecasted_series)-1):
    y = y+1
    date_temp = index_for_forcaste[-1]
    if(is_leap_year(date_temp.year)):
      date_temp = date_temp + timedelta(days = 366)
    else:
      date_temp = date_temp + timedelta(days = 365)
    index_for_forcaste.append(date_temp)

  forecasted_series.index = pd.to_datetime(index_for_forcaste)
  forecasted_series = pd.DataFrame({name_of_datetime_index_column:forecasted_series.index, name_of_forecasted_column:forecasted_series.values})
  forecasted_series.index = forecasted_series[name_of_datetime_index_column]
  forecasted_series = forecasted_series.drop(name_of_datetime_index_column, axis = 1)

  return forecasted_series

def forecast(country,npast_year = 0, nforecast_year = 5):

    series = read_csv('../processed_data/country_wise/data/'+str(country)+'.csv', header=0, index_col=0, parse_dates=True)
    first_time = True
    for parameter_to_forecast in series.columns:
        if parameter_to_forecast == 'year':
            pass
        else:
            # evaluate parameters
            p_values = [0, 1, 2, 4, 6]
            d_values = range(0, 3)
            q_values = range(0, 3)
            
            tdf = series[parameter_to_forecast].copy()
            tdf.index = series.index
            tdf = tdf.squeeze()
           
            # selecting best model using grid search
            best_cfg, best_score = evaluate_models(tdf.values, p_values, d_values, q_values)
            # Instantiate the model
           
            model = SARIMAX(series[parameter_to_forecast], order=best_cfg)

            # Fit the model
            results = model.fit()

            # Generate predictions
            forecasts = results.get_prediction(start=len(series)-npast_year-1,end = len(series)+nforecast_year-1)

            # Extract prediction mean
            mean_forecast_sarima = forecasts.predicted_mean

            # printing some summury and forecast
            #print(mean_forecast_arima)
            print(results.summary())

            to_plot=forecasted_series_to_df(series[parameter_to_forecast], mean_forecast_sarima, npast_year, str(parameter_to_forecast), "year")
            if first_time:
                first_time = False
                temp = to_plot.copy()
            else:
                temp=pd.merge(to_plot, temp, on = "year", how = 'right')

    # writting forecastes to the hard-disk
    temp.to_csv('../processed_data/country_wise/forecasted/'+str(country)+'.csv')

    return temp, series


for i, country in enumerate(countries):
    to_plot, series = forecast(country = country, npast_year = 0, nforecast_year = 15)