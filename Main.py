import streamlit as st
import datetime
import pandas as pd
import numpy as np
import requests


from datetime import date
# from datetime import datetime
from datetime import timedelta
from londonbssfront.params import *
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.let_it_rain import rain
from londonbssfront.styling import style_metric_cards


###############################################################################
###### THEMING

our_name='DockDockGo'
st.set_page_config(page_title=our_name, layout="wide")

## Titles

st.markdown("<h4 style='text-align: center; color:#333333 ;'>We are DockDockGo.</h4>", unsafe_allow_html=True)
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




###############################################################################
### ORIGIN AND DESTINATION INPUTS

col1, col2 = st.columns(2)

with col1:
    with stylable_container(
    key="container_with_border",
    css_styles="""
        {
            background-color: white;
            margin: auto;
            border: 1px solid rgba(49, 51, 65, 0.2);
            border-radius: 0.5rem;
            padding: calc(1em - 1px)
        }
        """,
):
        st.markdown("<h3 style='text-align: center; color: #333333 ;'>ORIGIN</h3>", unsafe_allow_html=True)
        st.text_input('AREA','North')
        origin_neighbourhood=st.text_input('NEIGHBORHOOD','Hoxton')
        origin_street=st.text_input('STREET','Shoreditch Park')

    # expander1=st.expander(label=' ',expanded=True)
    # st.subheader('ORIGIN')
    # expander1.markdown("<h3 style='text-align: center; color: #333333 ;'>ORIGIN</h3>", unsafe_allow_html=True)
    # expander1.text_input('AREA','North')
    # origin_neighbourhood=expander1.text_input('NEIGHBORHOOD','Hoxton')
    # origin_street=expander1.text_input('STREET','Shoreditch Park')


with col2:
    with stylable_container(
    key="container_with_border",
    css_styles="""
        {
            background-color: white;
            border: 1px solid rgba(49, 51, 65, 0.2);
            border-radius: 0.5rem;
            padding: calc(1em - 1px)
        }
        """,
):
        st.markdown("<h3 style='text-align: center; color: #333333 ;'>DESTINATION</h3>", unsafe_allow_html=True)
        st.text_input('AREA','East')
        destination_neighbourhood=st.text_input('NEIGHBORHOOD','Liverpool Street')
        destination_street=st.text_input('STREET','Finsbury Circus')

    # expander2=st.expander(label=' ',expanded=True)
    # expander2.markdown("<h3 style='text-align: center; color:#333333 ;'>DESTINATION</h3>", unsafe_allow_html=True)
    # # st.subheader('DESTINATION')
    # expander2.text_input('AREA','East')
    # destination_neighbourhood=expander2.text_input('NEIGHBORHOOD','Liverpool Street')
    # destination_street=expander2.text_input('STREET','Finsbury Circus')

st.divider()

###############################################################################
#### TIMING

with stylable_container(
    key="container_with_border",
    css_styles="""
        {
            background-color: white;
            margin: auto;
            border: 1px solid rgba(49, 51, 65, 0.2);
            border-radius: 0.5rem;
            padding: calc(1em - 1px)
        }
        """,
):
        st.markdown("<h3 style='text-align: center; color: #333333 ;'>WHEN DO YOU NEED TO LEAVE</h3>", unsafe_allow_html=True)
        timing=st.time_input(' ',datetime.time(1, 00),step=3600)


st.divider()

###############################################################################
### Connecting to the API

##### CODE

### REAL TIME NUMBERS CODE
origin=origin_street+", "+origin_neighbourhood
destination=destination_street+", "+destination_neighbourhood

response= requests.get('https://api.tfl.gov.uk/BikePoint/')
stations = response.json()


for station in stations:
    if station['commonName']==origin:
        origin_lat=station['lat']
        origin_lon=station['lon']
        for add_property in station['additionalProperties']:
            if add_property['key'] == 'NbBikes':
                nb_bikes=add_property['value']

for station in stations:
    if station['commonName']==destination:
        destination_lat=station['lat']
        destination_lon=station['lon']
        for add_property in station['additionalProperties']:
            if add_property['key'] == 'NbEmptyDocks':
                nb_empty_docks=add_property['value']

#### ITINERARY CODE

stations_df=pd.read_csv('raw_data/stations_df_st.csv')

# stations_dict={'Stations': [origin, destination],
#                'Latitude': [origin_lat,destination_lat],
#                'Longitude':[origin_lon,destination_lon]}

# stations_points=pd.DataFrame(stations_dict)

## ITINERARY JOURNEY

url=f'https://api.tfl.gov.uk/Journey/JourneyResults/{origin_lat},{origin_lon}/to/{destination_lat},{destination_lon}'
parameters_iti={'mode':'cycle','cyclepreference':'AllTheWay'}
response_iti= requests.get(url,params=parameters_iti)
journey=response_iti.json()

steps=journey['journeys'][0]['legs'][0]['instruction']['steps']

steps_lat=[origin_lat]
steps_lon=[origin_lon]
for step in steps:
    steps_lat.append(step['latitude'])
    steps_lon.append(step['longitude'])

steps_lat.append(destination_lat)
steps_lon.append(destination_lon)

steps_lat_extra=[origin_lat]
steps_lon_extra=[origin_lon]

for i in range(1,len(steps_lat)-1):
   steps_lat_extra+=list(np.linspace(steps_lat[i-1],steps_lat[i],30))
   steps_lon_extra+=list(np.linspace(steps_lon[i-1],steps_lon[i],30))

steps_lat_extra.append(destination_lat)
steps_lon_extra.append(destination_lon)

itinerary_df=pd.DataFrame()
itinerary_df['lat']=steps_lat_extra
itinerary_df['lon']=steps_lon_extra

size_iti=[60]
for i in range(itinerary_df.shape[0]-2):
    size_iti+=[15]
size_iti+=[60]

color_iti=['#d30000']
for i in range(itinerary_df.shape[0]-2):
    color_iti+=['#d30000']
color_iti+=['#d30000']

itinerary_df['size']=size_iti
itinerary_df['color']=color_iti

## ITINERARY DURATION

duration_cycle=journey['journeys'][0]['legs'][0]['duration']

parameters_walking={'mode':'walking'}
response_2= requests.get(url,params=parameters_walking)
journey_2=response_2.json()
duration_walking=journey_2['journeys'][0]['legs'][0]['duration']



#### WEATHER CODE

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


#### CLOSEST STATIONS CODE

stations_f_closest=pd.read_csv('raw_data/stations_f_closest.csv')
for row in stations_f_closest.iterrows():
    if row[1]['Station_name']==origin:
        closest_origin=row[1]['Closest_name']
    if row[1]['Station_name']==destination:
        closest_destination=row[1]['Closest_name']


for station in stations:
    if station['commonName']==closest_origin:
        origin_lat=station['lat']
        origin_lon=station['lon']
        for add_property in station['additionalProperties']:
            if add_property['key'] == 'NbBikes':
                nb_bikes_closest_origin=add_property['value']

for station in stations:
    if station['commonName']==closest_destination:
        destination_lat=station['lat']
        destination_lon=station['lon']
        for add_property in station['additionalProperties']:
            if add_property['key'] == 'NbEmptyDocks':
                nb_empty_docks_closest_destination=add_property['value']

##### IN THE ST

#### REAL TIME NUMBERS

if st.button('Predict'):

    # rain(
    #     emoji='https:'+icon,
    #     font_size=54,
    #     falling_speed=5,
    #     animation_length=2,
    # )


    st.markdown("<h3 style='text-align: center; color: #333333 ;'>PREDICTION</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        with stylable_container(
            key="container_with_border",
            css_styles="""
                {
                    background-color: white;
                    margin: auto;
                    border: 1px solid rgba(49, 51, 65, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                }
                """,
            ):
            st.markdown("<h3 style='text-align: center; color:#333333 ;'>ORIGIN</h3>", unsafe_allow_html=True)
            st.metric(label="AVAILABLE BIKES", value=nb_bikes)

    with col2:
        with stylable_container(
            key="container_with_border",
            css_styles="""
                {
                    background-color: white;
                    margin: auto;
                    border: 1px solid rgba(49, 51, 65, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                }
                """,
            ):
            st.markdown("<h3 style='text-align: center; color:#333333 ;'>DESTINATION</h3>", unsafe_allow_html=True)
            st.metric(label="EMPTY DOCKS", value=nb_empty_docks)


#### MAP and ITINERARY

    st.markdown("<h3 style='text-align: center; color:#333333 ;'>ITINERARY</h3>", unsafe_allow_html=True)
    st.map(data=itinerary_df,latitude='lat',longitude='lon',zoom=13,size='size',color='color')

    with stylable_container(
            key="container_with_border",
            css_styles="""
                {
                    background-color: white;
                    margin: auto;
                    border: 1px solid rgba(49, 51, 65, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                }
                """,
            ):

        st.markdown("<h3 style='text-align: center; color: #333333 ;'>TRIP DURATION COMPARISON</h3>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label='CYCLING',value=str(duration_cycle)+' min')

        with col2:
            st.metric(label='WALKING',value=str(duration_walking)+' min')



#### WEATHER
    with stylable_container(
            key="container_with_border",
            css_styles="""
                {
                    background-color: white;
                    margin: auto;
                    border: 1px solid rgba(49, 51, 65, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                }
                """,
            ):

        st.markdown("<h3 style='text-align: center; color: #333333 ;'>WEATHER FORECAST</h3>", unsafe_allow_html=True)

        col1, col2,col3,col4 = st.columns(4)
        with col1:
            st.metric(label='TEMPERATURE',value=str(temperature)+'°C')

        with col2:
            st.metric(label='CONDITION',value=condition)

        with col3:
            st.metric(label='PROBABILITY', value=str(prob_rain)+'%')

        with col4:
            st.image('https:'+icon)

##### CLOSEST STATIONS

    with stylable_container(
            key="container_with_border",
            css_styles="""
                {
                    background-color: white;
                    margin: auto;
                    border: 1px solid rgba(49, 51, 65, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                }
                """,
            ):

        if nb_bikes==0 and nb_empty_docks!=0:
            st.markdown("<h4 style='text-align: center; color: #333333 ;'>'CLOSEST ORIGIN STATION'</h4>", unsafe_allow_html=True)
            st.write(closest_origin)
            st.metric(label="AVAILABLE BIKES", value=nb_bikes_closest_origin)


        elif nb_bikes==0 and nb_empty_docks!=0:
            st.markdown("<h4 style='text-align: center; color: #333333 ;'>'CLOSEST DESTINATION STATION'</h4>", unsafe_allow_html=True)
            st.write(closest_destination)
            st.metric(label="EMPTY DOCKS", value=nb_empty_docks_closest_destination)

        elif nb_bikes==0 and nb_empty_docks!=0:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<h4 style='text-align: center; color: #333333 ;'>'CLOSEST ORIGIN STATION'</h4>", unsafe_allow_html=True)
                st.write(closest_origin)
                st.metric(label="AVAILABLE BIKES", value=nb_bikes_closest_origin)

            with col2:
                st.markdown("<h4 style='text-align: center; color: #333333 ;'>'CLOSEST DESTINATION STATION'</h4>", unsafe_allow_html=True)
                st.write(closest_destination)
                st.metric(label="EMPTY DOCKS", value=nb_empty_docks_closest_destination)

    ### This is for test, remove
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader('CLOSEST ORIGIN STATION')
                st.write(closest_origin)
                st.metric(label="AVAILABLE BIKES", value=nb_bikes_closest_origin)

            with col2:
                st.subheader('CLOSEST DESTINATION STATION')
                st.write(closest_destination)
                st.metric(label="EMPTY DOCKS", value=nb_empty_docks_closest_destination)
