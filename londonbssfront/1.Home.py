import streamlit as st
import datetime
import pandas as pd
import numpy as np


# [theme]

# primaryColor="#6eb52f"
# backgroundColor="#f0f0f5"
# secondaryBackgroundColor="#e0e0ef"
# textColor="#262730"
# font="sans serif"

st.set_page_config(layout="wide")

## Titles

st.title('London Bike Sharing System')

### Inputs
st.subheader('Destination')

st.time_input('I will leave in:', datetime.time(1, 00))

####




### Maps

# df = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#     columns=['lat', 'lon'])

# st.map(df)
st.map(latitude='51.5072', longitude='0.1276')
