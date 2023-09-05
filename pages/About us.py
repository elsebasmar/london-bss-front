import streamlit as st
from londonbssfront.styling import add_logo_2
from PIL import Image


our_name='DockDockGo'
st.set_page_config(page_title='About_Us', layout="wide")
Logo= Image.open('raw_data/Logo.png')
Logo_url='raw_data/Logo.png'


add_logo_2()
with st.sidebar.container():
    st.image(Logo,width=100)

st.header('We are '+our_name)
