import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_extras.stylable_container import stylable_container


our_name='DockDockGo'
st.set_page_config(page_title='London_Map', layout="wide")

# logo_path=os.path.join(os.getcwd(),'londonbssfront','images')

Logo=Image.open('londonbssfront/images/Logo.png')
Logo_full=Image.open('londonbssfront/images/DDGLogo.png'))


col1, col2, col3, col4,col5,col6,col7,col8,col9= st.columns(9)
with col9:
    st.image(Logo, use_column_width=True)

# add_logo_2()
# with st.sidebar.container():
#     st.image(Logo,width=100)
# stations_path=os.path.join(os.getcwd(),'londonbssfront','stations_csv')

stations_df_st=pd.read_csv('londonbssfront/stations_csv/stations_df_st.csv')

# with stylable_container(
#         key="container_with_border",
#         css_styles="""
#             {
#                 background-color: white;
#                 border: 1px solid rgba(49, 51, 65, 0.2);
#                 border-radius: 0.5rem;
#                 padding: calc(1em - 1px)
#             }
#             """,
#         ):
st.markdown("<h2 style='text-align: center; color:#6d6d6d ;'>LONDON MAP</h2>", unsafe_allow_html=True)

st.map(data=stations_df_st,latitude='s_lat',longitude='s_lon',color='#ff000080',zoom=11,size='Size_bucket',use_container_width=True)
