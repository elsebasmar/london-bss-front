import streamlit as st

# hide = """
# <style>
# ul.streamlit-expander {
#     border: 0 !important;
# </style>
# """

# st.markdown(
#     '''
#     <style>
#     .streamlit-expanderHeader {
#         background-color: #f0f0f0;
#         color: #6d6d6d; # Adjust this for expander header color
#     }
#     .streamlit-expanderContent {
#         background-color: white;
#         color: black; # Expander content color
#     }
#     </style>
#     ''',
#     unsafe_allow_html=True
# )

# st.markdown(hide, unsafe_allow_html=True)


# st.markdown("""
# <style>
# div[data-testid="metric-container"] {
#    background-color: white;
#    border: 1px solid rgba(28, 131, 225, 0.1);
#    padding: 5% 5% 5% 10%;
#    border-radius: 5px;
#    color: #d30000;
#    overflow-wrap: break-word;
# }

# /* breakline for metric text         */
# div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
#    overflow-wrap: break-word;
#    white-space: break-spaces;
#    color: #6d6d6d;
# }
# </style>
# """
# , unsafe_allow_html=True)


# with stylable_container(
# key="text",
# css_styles="""
# timeinput {
#     background-color: green;
#     color: white;
#     border-radius: 20px;
# }
# """,
# ):
#     timing=st.time_input('(IN HOURS)',datetime.time(1, 00),step=3600)
