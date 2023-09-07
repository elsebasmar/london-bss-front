import streamlit as st
from londonbssfront.styling import add_logo_2
from PIL import Image


our_name='DockDockGo'
st.set_page_config(page_title='About_Us', layout="wide")

# logo_path=os.path.join(os.getcwd(),'londonbssfront','images')

Logo=Image.open('londonbssfront/images/Logo.png')
Logo_full=Image.open('londonbssfront/images/DDG_logo.png')

col1, col2, col3, col4,col5,col6,col7,col8,col9= st.columns(9)
with col9:
    st.image(Logo, use_column_width=True)
