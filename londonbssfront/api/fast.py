import pandas as pd
import darts
from darts.models import AutoARIMA
from darts import TimeSeries
import math


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.state.eagle_wharf = AutoARIMA.load("saved_models/eagle_wharf_road__hoxton_model_correct_data_encoded.pkl")
app.state.finsbury_circus = AutoARIMA.load("saved_models/finsbury_circus__liverpool_street_model_correct_data_encoded.pkl")
app.state.wennlock_road = AutoARIMA.load("saved_models/wenlock_road___hoxton_model_correct_data_encoded.pkl")
app.state.wormwood_street = AutoARIMA.load("saved_models/wormwood_street__liverpool_street_model_correct_data_encoded.pkl")


@app.get("/predict")
def predict(
    origin_m: str,
    destination_m: str,
    timing: str
    ):
    # Convert to int
    timing = int(timing)


    # Load origin station data
    origin_full_df = pd.read_csv(f'londonbssfront/models_csv/processed_all_{origin_m}_2020-01-01_2023-06-19_full_data_4.csv')
    origin_full_df['startdate'] = pd.to_datetime(origin_full_df['startdate']).dt.tz_localize(None)
    origin_full_df.drop(columns=['year', 'month', 'day', 'hour', 'weekday'], inplace=True)

    # Load correct model
    if origin_m == "eagle_wharf_road__hoxton":
        origin_model_loaded = app.state.eagle_wharf
    elif origin_m == "finsbury_circus__liverpool_street":
        origin_model_loaded = app.state.finsbury_circus
    elif origin_m == "wenlock_road___hoxton":
        origin_model_loaded = app.state.wennlock_road
    elif origin_m == "wormwood_street__liverpool_street":
        origin_model_loaded = app.state.wormwood_street

    # Model Params
    covariates = ['elisabeth_line', 'lockdown','strike', 'school_holidays', 'daytime', 'London_zone_Central',
        'London_zone_North', 'London_zone_West', 'London_zone_South_West',
        'London_zone_South_East', 'London_zone_East', 'Event', 'temperature',
        'rainfall', 'snowfall', 'cloudcover', 'wind_speed', 'wind_direction']

    origin_cov_series = TimeSeries.from_dataframe(origin_full_df, time_col='startdate', value_cols=covariates, fill_missing_dates=True, freq='H', fillna_value=0)

    # The actual prediction for origin
    origin_prediction = origin_model_loaded.predict(timing,future_covariates=origin_cov_series)
    origin_result = sum(origin_prediction.pd_series())
    if origin_result > 0.5:
        origin_result = math.ceil(origin_result)
    else:
        origin_result = math.floor(origin_result)

    # Load destination station
    destination_full_df = pd.read_csv(f'londonbssfront/models_csv/processed_all_{destination_m}_2020-01-01_2023-06-19_full_data_4.csv')
    destination_full_df['startdate'] = pd.to_datetime(destination_full_df['startdate']).dt.tz_localize(None)
    destination_full_df.drop(columns=['year', 'month', 'day', 'hour', 'weekday'], inplace=True)

    # Choose destination model
    if destination_m == "eagle_wharf_road__hoxton":
        destination_model_loaded = app.state.eagle_wharf
    elif destination_m == "finsbury_circus__liverpool_street":
        destination_model_loaded = app.state.finsbury_circus
    elif destination_m == "wenlock_road___hoxton":
        destination_model_loaded = app.state.wennlock_road
    elif destination_m == "wormwood_street__liverpool_street":
        destination_model_loaded = app.state.wormwood_street

    destination_cov_series = TimeSeries.from_dataframe(destination_full_df, time_col='startdate', value_cols=covariates, fill_missing_dates=True, freq='H', fillna_value=0)

    destination_prediction = destination_model_loaded.predict(timing + 1,future_covariates=destination_cov_series)
    destination_result = sum(destination_prediction.pd_series())

    if destination_result > 0.5:
        destination_result = math.ceil(destination_result)
    else:
        destination_result = math.floor(destination_result)

    return {"origin_station": origin_result, "destination_station": destination_result}
