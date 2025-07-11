import streamlit as st

st.set_page_config(
    layout="wide", initial_sidebar_state="auto", menu_items=None,
    page_icon="📊", page_title='Game Sales Dashboard',
)
hide_streamlit_style = """
            <style>
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- PAGE SETUP ---
sales  = st.Page(
    page="views/vgcharts.py",
    title="Game Sales",
    icon=":material/finance:",
    default=True
)

platforms  = st.Page(
    page="views/platforms.py",
    title="Platforms",
    icon=":material/videogame_asset:",
)

generations  = st.Page(
    page="views/generations.py",
    title="Generations",
    icon=":material/history:",
)

# --- NAVIGATION SETUP ---
pg = st.navigation(
    {
        "vgcharts": [sales],
        "uvlist": [platforms, generations]
    }
    )

# --- RUN NAGIVATION ---
pg.run()
