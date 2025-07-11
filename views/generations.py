import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
import sqlite3

# ========== Styles ============ #
# colors = [
#     '#3366CC', '#DC3912', '#FF9900', '#109618', '#990099',
#     '#0099C6', '#DD4477', '#66AA00', '#B82E2E', '#316395'
# ]
colors =     ['rgb(27,158,119)', 'rgb(217,95,2)',  'rgb(0, 128, 0)' , 'rgb(231,41,138)', 'rgb(102,166,30)',
            'rgb(255, 0, 255)', 'rgb(166,118,29)', 'rgb(102,102,102)',  'rgb(55,126,184)', 'rgb(228,26,28)',
                'rgb(117,112,179)', 'rgb(0, 255, 255)', 'rgb(230,171,2)'  , 'rgb(75, 0, 130)', 'rgb(255, 20, 147)',  
                'rgb(255, 99, 71)', 'rgb(30, 144, 255)', 'rgb(218, 165, 32)', 'rgb(153, 153, 51)', 'rgb(255, 127, 0)'
            ]

tab_card = {'height': '100%'}
main_config = {
    "hovermode": "x unified",
    "legend": {"yanchor": "top",
               "y": 0.9,
               "xanchor": "left",
               "x": 0.1,
               "title": {"text": None},
               "font": {"color": "white"},
               "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l": 10, "r": 0, "t": 25, "b": 0}
}

conn = sqlite3.connect('data/games_data.db')

@st.cache_data
def get_labels(_conn):
    gen_labels = pd.read_sql(f"SELECT DISTINCT Gen FROM platform_id WHERE Gen IS NOT NULL ORDER BY Gen" , _conn)
    return gen_labels

@st.cache_data
def get_gen_data(gen, _conn):
    # Load data from Google BigQuery or a CSV file
    game_df = pd.read_sql(f"""SELECT * FROM platform_id WHERE Gen = '{gen}'""", _conn)
    return game_df

information = {
    "Name": "Consoles",
    "Year": "Ano de Lançamento",
    "Year_end": "Final da Fabricação",
    "Type": "Modelo",
}

# @st.cache_data
# def get_plat_summary_data(developer, _conn):
#     # Load data from Google BigQuery or a CSV file
#     plat_sum_df = pd.read_sql(f"""SELECT * FROM platform_id WHERE Developer = '{developer}'""",_conn)
#     # conn.close()
#     return plat_sum_df

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">',
                unsafe_allow_html=True)

remote_css(
    "https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css")


st.header("Gerações")

def main():

    st.selectbox(
                'Gerações de Consoles',
                # on_change=filter_update,
                key='Gen',
                options=(labels)
            )
    gen_df = get_gen_data(st.session_state['Gen'], conn)
    st.dataframe(gen_df)
    # Initialize the HTML structure for the statistics
    table_information = """
    <div class="ui small statistics">"""

    # Add the label for the information
    table_information += """
        <div class='grey statistic'>
            <div class='value'>"""+information['Name']+"""</div>"""

    # Iterate through the DataFrame and add each game name
    for i in gen_df.index:
        table_information += """<div class='label'>""" + str(gen_df['Name'].iloc[i])[:25]+"""</div>""" if str(gen_df['Name'].iloc[i]) != 0 else ""

    # Close the div tags
    table_information += """
        </div>
    </div>"""
    st.markdown(table_information, unsafe_allow_html=True)





if __name__ == "__main__":
    labels = get_labels(conn)
    

    main()  
    