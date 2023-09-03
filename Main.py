import streamlit as st
import datetime
import pandas as pd
import numpy as np
import requests


from datetime import date
# from datetime import datetime
from datetime import timedelta
from londonbssfront.params import *

###### THEMING

st.set_page_config(page_title='QuickDock', layout="wide")

## Titles

st.markdown("<h4 style='text-align: center; color:#333333 ;'>We are QUICKDOCK.</h4>", unsafe_allow_html=True)
# st.divider()

hide = """
<style>
ul.streamlit-expander {
    border: 0 !important;
</style>
"""

st.markdown(
    '''
    <style>
    .streamlit-expanderHeader {
        background-color: #f0f0f0;
        color: #6d6d6d; # Adjust this for expander header color
    }
    .streamlit-expanderContent {
        background-color: white;
        color: black; # Expander content color
    }
    </style>
    ''',
    unsafe_allow_html=True
)
st.markdown(hide, unsafe_allow_html=True)

### ORIGIN AND DESTINATION INPUTS

col1, col2 = st.columns(2)

with col1:
    expander=st.expander(label=' ',expanded=True)
    # st.subheader('ORIGIN')
    expander.markdown("<h3 style='text-align: center; color: #333333 ;'>ORIGIN</h3>", unsafe_allow_html=True)
    expander.text_input('AREA','North')
    origin_neighbourhood=expander.text_input('NEIGHBORHOOD','Hoxton')
    origin_street=expander.text_input('STREET','Shoreditch Park')


with col2:
    expander=st.expander(label=' ',expanded=True)
    expander.markdown("<h3 style='text-align: center; color:#333333 ;'>DESTINATION</h3>", unsafe_allow_html=True)
    # st.subheader('DESTINATION')
    expander.text_input('AREA','East')
    destination_neighbourhood=expander.text_input('NEIGHBORHOOD','Liverpool Street')
    destination_street=expander.text_input('STREET','Finsbury Circus')

st.divider()

#### TIMING

st.markdown("<h3 style='text-align: center; color: #333333 ;'>WHEN DO YOU NEED TO LEAVE</h3>", unsafe_allow_html=True)
# expander=st.expander(label='TIMING',expanded=True)
timing=st.time_input(' ',datetime.time(1, 00),step=3600)


st.divider()

origin=origin_street+", "+origin_neighbourhood
destination=destination_street+", "+destination_neighbourhood

### Connecting to the API

response= requests.get('https://api.tfl.gov.uk/BikePoint/')
stations = response.json()


col1, col2 = st.columns(2)

for station in stations:
    if station['commonName']==origin:
        origin_lat=station['lat']
        origin_lon=station['lon']
        for add_property in station['additionalProperties']:
            if add_property['key'] == 'NbBikes':
                nb_bikes=add_property['value']

with col1:
    expander=st.expander(label=' ',expanded=True)
    expander.markdown("<h3 style='text-align: center; color:#333333 ;'>ORIGIN</h3>", unsafe_allow_html=True)
    expander.metric(label="AVAILABLE BIKES", value=nb_bikes)


for station in stations:
    if station['commonName']==destination:
        destination_lat=station['lat']
        destination_lon=station['lon']
        for add_property in station['additionalProperties']:
            if add_property['key'] == 'NbEmptyDocks':
                nb_empty_docks=add_property['value']

with col2:
    expander=st.expander(label=' ',expanded=True)
    expander.markdown("<h3 style='text-align: center; color:#333333 ;'>DESTINATION</h3>", unsafe_allow_html=True)
    expander.metric(label="EMPTY DOCKS", value=nb_empty_docks)


#### ITINERARY


stations_dict={'Stations': [origin, destination],
               'Latitude': [origin_lat,destination_lat],
               'Longitude':[origin_lon,destination_lon]}


stations_df=pd.DataFrame(stations_dict)

st.divider()

st.markdown("<h3 style='text-align: center; color:#333333 ;'>ITINERARY</h3>", unsafe_allow_html=True)
st.map(data=stations_df,latitude='Latitude',longitude='Longitude',zoom=12)

st.divider()

##### WEATHER

url_2='http://api.weatherapi.com/v1/forecast.json'
parameters={'key':WEATHER_KEY,'q':'London','days':2}
response_2= requests.get(url_2,params=parameters)
weather_2 = response_2.json()

from datetime import datetime

timing_datetime_day=(datetime.now()+timedelta(hours=int(timing.strftime("%H")))).strftime("%Y-%m-%d")
timing_datetime_full=(datetime.now()+timedelta(hours=int(timing.strftime("%H")))).strftime("%Y-%m-%d %H:00")

for day in weather_2['forecast']['forecastday']:
    if day['date']==timing_datetime_day:
        for hour in day['hour']:
            if hour['time']==timing_datetime_full:
                temperature=hour['temp_c']
                condition=hour['condition']['text']
                icon=hour['condition']['icon']
                prob_rain=hour['chance_of_rain']

st.markdown("<h3 style='text-align: center; color: #333333 ;'>WEATHER FORECAST</h3>", unsafe_allow_html=True)

col1, col2,col3,col4 = st.columns(4)
with col1:
    st.metric(label='TEMPERATURE',value=str(temperature)+'°C')

with col2:
    st.metric(label='Condition',value=condition)

with col3:
    st.image('https:'+icon)


with col4:
    st.metric(label='Probability of Rain', value=str(prob_rain)+'%')




##### CLOSEST STATIONS

st.divider()

st.markdown("<h3 style='text-align: center; color: #333333 ;'>CLOSEST STATIONS</h3>", unsafe_allow_html=True)
stations_f_closest=pd.read_csv('raw_data/stations_f_closest.csv')

col1, col2 = st.columns(2)

with col1:
    st.subheader('CLOSEST ORIGIN STATION')
    for row in stations_f_closest.iterrows():
        if row[1]['Station_name']==origin:
            st.write(row[1]['Closest_name'])


with col2:
    st.subheader('CLOSEST DESTINATION STATION')
    for row in stations_f_closest.iterrows():
        if row[1]['Station_name']==destination:
            st.write(row[1]['Closest_name'])
