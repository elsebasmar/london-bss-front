import streamlit as st
import datetime
import pandas as pd
import numpy as np
import requests


###### Theme and Formatting

st.set_page_config(page_title='TBD', layout="wide")

## Titles

st.title('Time to fix all your bike problems')

### Inputs

col1, col2 = st.columns(2)

with col1:
    st.subheader('Origin')
    st.text_input('Origin Area','North')
    origin_neighbourhood=st.text_input('Origin Neighborhood','Hoxton')
    origin_street=st.text_input('Origin Street','Shoreditch Park')

with col2:
    st.subheader('Destination')
    st.text_input('Destination Area','East')
    destination_neighbourhood=st.text_input('Destination Neighborhood','Liverpool Street')
    destination_street=st.text_input('Destination Street','Finsbury Circus')

st.subheader('Are you late to work again??')

st.time_input('Yes, I will leave in:', datetime.time(1, 00))

####

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
    st.subheader('Can you find a bike to save your day')
    st.metric(label="Available bikes", value=nb_bikes)


for station in stations:
    if station['commonName']==destination:
        destination_lat=station['lat']
        destination_lon=station['lon']
        for add_property in station['additionalProperties']:
            if add_property['key'] == 'NbEmptyDocks':
                nb_empty_docks=add_property['value']

with col2:
    st.subheader('BUT Can you drop your bike?')
    st.metric(label="Empty docks", value=nb_empty_docks)


#### Illustrative Map

stations_dict={'Stations': [origin, destination],
               'Latitude': [origin_lat,destination_lat],
               'Longitude':[origin_lon,destination_lon]}


stations_df=pd.DataFrame(stations_dict)

st.map(data=stations_df,latitude='Latitude',longitude='Longitude',zoom=15)
