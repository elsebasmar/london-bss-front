import streamlit as st

# def style_metric_cards(
#     background_color: str = "#FFF",
#     border_size_px: int = 1,
#     border_color: str = "#CCC",
#     border_radius_px: int = 5,
#     border_left_color: str = "#9AD8E1",
#     box_shadow: bool = True,
# ):

#     box_shadow_str = (
#         "box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;"
#         if box_shadow
#         else "box-shadow: none !important;"
#     )
#     st.markdown(
#         f"""
#         <style>
#             div[data-testid="metric-container"] {{
#                 background-color: {background_color};
#                 border: {border_size_px}px solid {border_color};
#                 padding: 5% 5% 5% 10%;
#                 border-radius: {border_radius_px}px;
#                 border-left: 0.5rem solid {border_left_color} !important;
#                 {box_shadow_str}
#             }}
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

def add_logo_2():
    st.markdown(
        f"""
        <style>
                [data-testid="stSidebarNav"]::before {{
                content: "DockDockGo";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
                color:white;
            }}
        </style>
        
        """,
        unsafe_allow_html=True,
    )

from PIL import Image
import streamlit as st

# You can always call this function where ever you want

def add_logo_3(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

# my_logo = add_logo(logo_path="your/logo/path", width=50, height=60)


# OR
