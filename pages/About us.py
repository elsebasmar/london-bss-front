import streamlit as st
from londonbssfront.styling import add_logo_2
from PIL import Image


our_name='DockDockGo'
st.set_page_config(page_title='About_Us', layout="wide")
Logo= Image.open('raw_data/Logo.png')
Logo_url='raw_data/Logo.png'

col1, col2, col3, col4,col5,col6,col7,col8,col9= st.columns(9)
with col9:
    st.image(Logo, use_column_width=True)
