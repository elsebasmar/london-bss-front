import streamlit as st
import pandas as pd
import numpy as np
from londonbssfront.styling import add_logo_2
from PIL import Image

our_name='DockDockGo'
st.set_page_config(page_title='London_Map', layout="wide")
Logo= Image.open('raw_data/Logo.png')
Logo_url='raw_data/Logo.png'


add_logo_2()
with st.sidebar.container():
    st.image(Logo,width=100)

## Titles

st.title('LONDON BIKE STATIONS')

stations_df_st=pd.read_csv('raw_data/stations_df_st.csv')

# color_dict={'Area_loc': list(stations_df_st['Area_loc'].unique())
#                        , 'Colours': ['#ffbaba','#ff7b7b', '#ff5252', '#ff0000', '#a70000']
#                     ,'index':[0, 1, 2, 3,4]}

# color_df=pd.DataFrame(color_dict)

# stations_df_st_2=stations_df_st.merge(color_df,on='Area_loc',how='left')

st.map(data=stations_df_st,latitude='s_lat',longitude='s_lon',color='#ff000080',zoom=11,size='Size_bucket',use_container_width=True)
