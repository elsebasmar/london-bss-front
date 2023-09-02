import streamlit as st
import pandas as pd


st.set_page_config(layout="wide")

## Titles

st.title('BIKES BIKES BIKES')

stations_df_st=pd.read_csv('raw_data/stations_df_st.csv')

# color_dict={'Area_loc': list(stations_df_st['Area_loc'].unique())
#                        , 'Colours': ['#ffbaba','#ff7b7b', '#ff5252', '#ff0000', '#a70000']
#                     ,'index':[0, 1, 2, 3,4]}

# color_df=pd.DataFrame(color_dict)

# stations_df_st_2=stations_df_st.merge(color_df,on='Area_loc',how='left')

st.map(data=stations_df_st,latitude='s_lat',longitude='s_lon',color='Colours',zoom=11,size='Size_bucket')
