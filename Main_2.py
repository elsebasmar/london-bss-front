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
from londonbssfront.styling import add_logo_2
from londonbssfront.styling import add_logo_3
from streamlit_extras.app_logo import add_logo
from PIL import Image
from streamlit_extras.colored_header import colored_header
from londonbssfront.distance import dist,find_nearest


###############################################################################
###### THEMING

our_name='DockDockGo.'
st.set_page_config(page_title=our_name, layout="wide")
Logo= Image.open('raw_data/Logo.png')
Logo_url='raw_data/Logo.png'

add_logo_2()

with st.sidebar.container():
    st.image(Logo,width=100)

col1, col2, col3, col4,col5,col6,col7,col8,col9= st.columns(9)

with col5:
    st.image(Logo, use_column_width=True)


### METRIC MARKDOWN

st.markdown("""
<style>
div[data-testid="metric-container"] {
   background-color: #f0f0f0;
   padding: 5% 5% 5% 10%;
   color: #d30000;
   max-width=10px;
}

/* breakline for metric text         */
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
   color: #6d6d6d;
}
</style>
"""
, unsafe_allow_html=True)

##############################################################################
### CALLING API

url = "https://nominatim.openstreetmap.org"
stations_df=pd.read_csv('raw_data/stations_df_st.csv')


###############################################################################
### ORIGIN AND DESTINATION INPUTS

col1, col2 = st.columns(2)

with col1:
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
        st.markdown("<h3 style='text-align: center; color: #333333 ;'>ORIGIN</h3>", unsafe_allow_html=True)
        with stylable_container(
    key="textinput",
    css_styles="""
        textinput {
            border-radius: 20px;
        }
        """,
):
            origin_address=st.text_input(' ','N1 7FZ')
            params = {
                    'q': origin_address,
                    'format': 'json'
                }
            response = requests.get(url,params=params).json() # TEXT -> [] / {}
            lat_origin=response[0]['lat']
            lon_origin=response[0]['lon']
            origin=find_nearest(float(lat_origin),float(lon_origin),stations_df)




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
        with stylable_container(
    key="textinput",
    css_styles="""
        textinput {
            border-radius: 20px;
        }
        """,
):
            destination_address=st.text_input(' ','EC2N 2DB')
            params = {
                    'q': destination_address,
                    'format': 'json'
                }
            response = requests.get(url,params=params).json() # TEXT -> [] / {}
            lat_destination=response[0]['lat']
            lon_destination=response[0]['lon']
            destination=find_nearest(float(lat_destination),float(lon_destination),stations_df)






##############################################################################

st.divider()

###############################################################################
#### TIMING

with stylable_container(
    key="container_with_border",
    css_styles="""
        {
            max-width:2000px;
            background-color: white;
            border: 1px solid rgba(49, 51, 65, 0.2);
            border-radius: 1rem;
            padding: 0.5em;  /* Adjusted padding here */

        }
        """,
):
        st.markdown("<h3 style='text-align: center; color: #333333 ;'>WHEN DO YOU NEED TO LEAVE</h3>", unsafe_allow_html=True)
        with stylable_container(
    key="timeinput",
    css_styles="""
        timeinput {
            border-radius: 20px;
        }
        """,
):
            timing=st.time_input('(IN HOURS)',datetime.time(1, 00),step=3600)


st.divider()

###############################################################################
### Connecting to the API

##### CODE

### REAL TIME NUMBERS CODE

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


stations_f2_origin=stations_df.drop(stations_df[stations_df['Station_name']==origin].index[0],axis=0)
stations_f2_destination=stations_df.drop(stations_df[stations_df['Station_name']==destination].index[0],axis=0)

closest_origin=find_nearest(float(lat_origin),float(lon_origin),stations_f2_origin)
closest_destination=find_nearest(float(lat_destination),float(lon_destination),stations_f2_destination)

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



        st.markdown("<h3 style='text-align: center; color: #333333 ;'>PREDICTION</h3>", unsafe_allow_html=True)




        col1, col2 = st.columns(2)

        with col1:
            with stylable_container(
                key="container_with_border_grey",
                css_styles="""
                    {
                        background-color: #f0f0f0;
                        margin: auto;
                        border: 1px solid rgba(49, 51, 65, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px)
                    }
                    """,
                ):
                st.markdown(f"<h3 style='text-align: center; color:#333333 ;'>{origin}</h3>", unsafe_allow_html=True)
                with stylable_container(
        key="metricinput",
        css_styles="""
            metricinput {
                border-radius: 20px;
            }
            """,
    ):
                    st.metric(label="AVAILABLE BIKES", value=nb_bikes)

        with col2:
            with stylable_container(
                key="container_with_border_grey",
                css_styles="""
                    {
                        background-color: #f0f0f0;
                        margin: auto;
                        border: 1px solid rgba(49, 51, 65, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px)
                    }
                    """,
                ):
                with stylable_container(
        key="metricinput",
        css_styles="""
            metricinput {
                border-radius: 20px;
            }
            """,
    ):
                    st.markdown(f"<h3 style='text-align: center; color:#333333 ;'>{destination}</h3>", unsafe_allow_html=True)
                    st.metric(label="EMPTY DOCKS", value=nb_empty_docks)

    st.divider()

#### MAP and ITINERARY


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
        with stylable_container(
        key="metricinput",
        css_styles="""
            metricinput {
                border-radius: 20px;
            }
            """,
    ):

            st.markdown("<h3 style='text-align: center; color:#333333 ;'>ITINERARY</h3>", unsafe_allow_html=True)
            st.map(data=itinerary_df,latitude='lat',longitude='lon',zoom=12.5,size='size',color='color',use_container_width=False)

    st.divider()


#### TRIP DURATION

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


        st.markdown("<h3 style='text-align: center; color: #333333 ;'>TRIP DURATION</h3>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            with stylable_container(
                key="container_with_border_grey",
                css_styles="""
                    {
                        background-color: #f0f0f0;
                        margin: auto;
                        border: 1px solid rgba(49, 51, 65, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px)
                    }
                    """,
                ):
                with stylable_container(
        key="metricinput",
        css_styles="""
            metricinput {
                border-radius: 20px;
            }
            """,
    ):

                    st.metric(label='CYCLING',value=str(duration_cycle)+' min')

        with col2:
            with stylable_container(
                key="container_with_border_grey",
                css_styles="""
                    {
                        background-color: #f0f0f0;
                        margin: auto;
                        border: 1px solid rgba(49, 51, 65, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px)
                    }
                    """,
                ):
                with stylable_container(
        key="metricinput",
        css_styles="""
            metricinput {
                border-radius: 20px;
            }
            """,
    ):
                    st.metric(label='WALKING',value=str(duration_walking)+' min')

    st.divider()

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


        col1, col2,col3,col4,col5,col6,col7,col8,col9= st.columns(9)
        with col5:
            st.markdown("<h3 style='text-align: center; color: #333333 ;'>WEATHER </h3>", unsafe_allow_html=True)

        with col6:
            st.image('https:'+icon,width=50)


        col1, col2,col3= st.columns(3)
        with col1:
            with stylable_container(
                key="container_with_border_grey",
                css_styles="""
                    {
                        background-color: #f0f0f0;
                        margin: auto;
                        border: 1px solid rgba(49, 51, 65, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px)
                    }
                    """,
                ):
                with stylable_container(
        key="metricinput",
        css_styles="""
            metricinput {
                border-radius: 20px;
            }
            """,
    ):
                    st.metric(label='TEMPERATURE',value=str(round(temperature,0))+'°C')

        with col2:
            with stylable_container(
                key="container_with_border_grey",
                css_styles="""
                    {
                        background-color: #f0f0f0;
                        margin: auto;
                        border: 1px solid rgba(49, 51, 65, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px)
                    }
                    """,
                ):
                with stylable_container(
        key="metricinput",
        css_styles="""
            metricinput {
                border-radius: 20px;
            }
            """,
    ):
                    st.metric(label='CONDITION',value=condition)

        with col3:
            with stylable_container(
                key="container_with_border_grey",
                css_styles="""
                    {
                        background-color: #f0f0f0;
                        margin: auto;
                        border: 1px solid rgba(49, 51, 65, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px)
                    }
                    """,
                ):
                with stylable_container(
        key="metricinput",
        css_styles="""
            metricinput {
                border-radius: 20px;
            }
            """,
    ):
                    st.metric(label='RAIN %', value=prob_rain)


    st.divider()

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

        st.markdown("<h3 style='text-align: center; color: #333333 ;'>CLOSEST STATIONS</h3>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            with stylable_container(
                key="container_with_border_grey",
                css_styles="""
                    {
                        background-color: #f0f0f0;
                        margin: auto;
                        border: 1px solid rgba(49, 51, 65, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px)
                    }
                    """,
                ):
                with stylable_container(
        key="metricinput",
        css_styles="""
            metricinput {
                border-radius: 20px;
            }
            """,
    ):
                    st.markdown(f"<h4 style='text-align: center; color: #333333 ;'>{closest_origin}</h4>", unsafe_allow_html=True)
                    st.metric(label="AVAILABLE BIKES", value=nb_bikes_closest_origin)

        with col2:
            with stylable_container(
                key="container_with_border_grey",
                css_styles="""
                    {
                        background-color: #f0f0f0;
                        margin: auto;
                        border: 1px solid rgba(49, 51, 65, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px)
                    }
                    """,
                ):
                with stylable_container(
        key="metricinput",
        css_styles="""
            metricinput {
                border-radius: 20px;
            }
            """,
            ):
                    st.markdown(f"<h4 style='text-align: center; color: #333333 ;'>{closest_destination}</h4>", unsafe_allow_html=True)
                    st.metric(label="EMPTY DOCKS", value=nb_empty_docks_closest_destination)

                # if nb_bikes==0 and nb_empty_docks!=0:
                #     st.markdown("<h4 style='text-align: center; color: #333333 ;'>'CLOSEST ORIGIN STATION'</h4>", unsafe_allow_html=True)
                #     st.write(closest_origin)
                #     st.metric(label="AVAILABLE BIKES", value=nb_bikes_closest_origin)


                # elif nb_bikes==0 and nb_empty_docks!=0:
                #     st.markdown("<h4 style='text-align: center; color: #333333 ;'>'CLOSEST DESTINATION STATION'</h4>", unsafe_allow_html=True)
                #     st.write(closest_destination)
                #     st.metric(label="EMPTY DOCKS", value=nb_empty_docks_closest_destination)

                # elif nb_bikes==0 and nb_empty_docks!=0:
                #     col1, col2 = st.columns(2)
                #     with col1:
                #         st.markdown("<h4 style='text-align: center; color: #333333 ;'>'CLOSEST ORIGIN STATION'</h4>", unsafe_allow_html=True)
                #         st.write(closest_origin)
                #         st.metric(label="AVAILABLE BIKES", value=nb_bikes_closest_origin)

                #     with col2:
                #         st.markdown("<h4 style='text-align: center; color: #333333 ;'>'CLOSEST DESTINATION STATION'</h4>", unsafe_allow_html=True)
                #         st.write(closest_destination)
                #         st.metric(label="EMPTY DOCKS", value=nb_empty_docks_closest_destination)

            # ### This is for test, remove
            #     else:
            #         col1, col2 = st.columns(2)
            #         with col1:
            #             st.subheader('CLOSEST ORIGIN STATION')
            #             st.write(closest_origin)
            #             st.metric(label="AVAILABLE BIKES", value=nb_bikes_closest_origin)

            #         with col2:
            #             st.subheader('CLOSEST DESTINATION STATION')
            #             st.write(closest_destination)
            #             st.metric(label="EMPTY DOCKS", value=nb_empty_docks_closest_destination)
