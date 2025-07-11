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
def get_initial_data(_conn):
    plat_df = pd.read_sql(f"SELECT * FROM platform_id", _conn)
    plat_df['Developer'] =  plat_df['Developer'].apply(lambda x: x if x != "-" else None)
    plat_df[['Developer', 'Type', 'Year', 'Games']] = plat_df[['Developer', 'Type', 'Year', 'Games']].fillna(0)
    plat_df['Year'] = plat_df['Year'].astype(int)
    
    # conn.close()
    return plat_df

@st.cache_data
def get_plat_data(platform, _conn):
    # Load data from Google BigQuery or a CSV file
    game_df = pd.read_sql(f"""SELECT game_image, name, url, publisher, developer,year
                          FROM game_info_v WHERE plat_name = '{platform}'""", _conn)
    game_df['game_image'] = game_df['game_image'].apply(lambda x: x.strip("'") if x else "https://media.istockphoto.com/id/1472933890/vector/no-image-vector-symbol-missing-available-icon-no-gallery-for-this-moment-placeholder.jpg?s=612x612&w=0&k=20&c=Rdn-lecwAj8ciQEccm0Ep2RX50FCuUJOaEM8qQjiLL0=")
    # conn.close()
    return game_df

@st.cache_data
def get_plat_summary_data(developer, _conn):
    # Load data from Google BigQuery or a CSV file
    plat_sum_df = pd.read_sql(f"""SELECT * FROM platform_id WHERE Developer = '{developer}'""",_conn)
    # conn.close()
    return plat_sum_df

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">',
                unsafe_allow_html=True)

remote_css(
    "https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css")


information = {
    "Developer": "Desenvolvedora",
    "Year": "Ano de Lançamento",
    "Games": "Jogos",
    "Type": "Modelo"
}

# Load the data
plat_df = get_initial_data(conn)

# Set the header for the app
st.header("Plataforma Wiki")

# Create a selectbox for platform selection
selected_platform = st.selectbox("Selecione a Plataforma:", options=plat_df['Name'], index=0)
game_df = get_plat_data(selected_platform, conn)

# Filter the DataFrame based on the selected platform
filtered_plat_df = plat_df.loc[plat_df['Name'] == selected_platform]


with st.expander("Informações sobre a plataforma", icon=":material/search:"):
    
    # Initialize the HTML structure for the scorecard
    table_scorecard = f"""
    <div class="ui small statistics">
    {
        "<div class='grey statistic'>"
            f"<div class='value'>{str(filtered_plat_df['Developer'].iloc[0])}</div>"
            f"<div class='label'>{information['Developer']}</div>"
        "</div>" if filtered_plat_df['Developer'].iloc[0] != 0 else ""
    }
    {
        "<div class='grey statistic'>"
            f"<div class='value'>{str(filtered_plat_df['Type'].iloc[0])}</div>"
            f"<div class='label'>{information['Type']}</div>"
        "</div>" if filtered_plat_df['Type'].iloc[0] != 0 else ""

    }
    {
        "<div class='grey statistic'>"
            f"<div class='value'>{str(filtered_plat_df['Year'].iloc[0])}</div>"
            f"<div class='label'>{information['Year']}</div>"
        "</div>" if filtered_plat_df['Year'].iloc[0] != 0 else ""
    }
    {
        "<div class='grey statistic'>"
            f"<div class='value'>{str(filtered_plat_df['Games'].iloc[0])}</div>"
            f"<div class='label'>{information['Games']}</div>"
        "</div>" if filtered_plat_df['Games'].iloc[0] != 0 else ""
    }
    """

    # Close the statistics div
    table_scorecard += """</div>"""

    # Render the HTML in Streamlit
    st.markdown(table_scorecard, unsafe_allow_html=True)

    # Progress bar based on status
    my_bar = st.progress(float(filtered_plat_df['Status'].iloc[0].strip("%")) / 100, text="Jogos encontrados")
    
    # Create columns for image and description
    _, img, _ = st.columns([0.2, 0.6, 0.2])
    desc = st.container()

    
        
    # Display image if it exists
    if not filtered_plat_df['img'].isna().iloc[0]:  # Check if the first image is not NaN
        img.image("https:" + filtered_plat_df['img'].iloc[0], width=400,
                  output_format="png",
                  caption=filtered_plat_df['Name'].iloc[0])  # Display the first image in the filtered DataFrame
    
    # Display description if it exists
    if not filtered_plat_df['description'].isna().iloc[0]:  # Check if the description is not NaN
        desc.markdown("<b>Descrição<b>", unsafe_allow_html=True)
        desc.write(filtered_plat_df['description'].iloc[0])

with st.expander("Gráficos", icon=":material/monitoring:"):
        # Criar um intervalo de anos e converter para int
        years_range = pd.period_range(start=int(game_df['year'].min()), end=int(game_df['year'].max()), freq='Y')
        years_range_int = years_range.year.astype(int)  # Converter para int

        # Contar o número de jogos por ano
        count_games = game_df[['year']].dropna().astype(int).groupby('year').size().reset_index(name='count_games')

        # Criar DataFrame a partir do intervalo de anos
        years_df = pd.DataFrame(years_range_int, columns=['year'])
        # Inicializar a coluna 'count_games' com 0
        years_df['count_games'] = 0

        if len(years_range) > 2:
            # Adicionar as contagens de jogos para os anos correspondentes
            for index, row in count_games.iterrows():
                years_df.loc[years_df['year'] == row['year'], 'count_games'] = row['count_games']

            # if max - min > 5: 
            fig_count_games = px.line(
                years_df, x="year", title="Jogos lançados pela plataforma por ano",
                y='count_games',
                # symbol="year",
                labels={'count_games': 'Jogos lançados', 'year': 'Ano', 'Platform':'Plataforma'},
                height=500,

                color_discrete_sequence=["#ff7c04"],
            )

            fig_count_games.update_layout(
                title=dict(font=dict(size=20)),
                # yaxis=dict(tickformat=".2f", ticksuffix='Mi', tickprefix='$'),
                # yaxis=dict(tickformat=".2f", ticksuffix='Mi'),
                
            )

            fig_count_games.update_layout(
                xaxis=dict(title=None, fixedrange=True),
                
                yaxis=dict(title=None, fixedrange=True),
                legend=dict(
                title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"
                )
            )

            fig_count_games.update_yaxes(
                showgrid=False, 
                color='black'
            )
            st.plotly_chart(fig_count_games, use_container_width=True,)

        plat_sum_df = get_plat_summary_data(str(filtered_plat_df['Developer'].iloc[0]), conn)
        plat_sum_df = plat_sum_df.dropna(subset=['Units'])

        if plat_sum_df.shape[0] > 1:
            categorias = sorted(plat_sum_df['Name'].drop_duplicates())
            discrete_colors = {categoria :colors[index] for index, categoria in enumerate(categorias)}
            plat_sum_df['Units'] = plat_sum_df['Units'].apply(
                lambda x: float(x.replace("K", "")) * 1000 if isinstance(x, str) and "K" in x 
                else (float(x.replace("M", "")) * 1000000 if isinstance(x, str) and "M" in x else float(0) )
            )

            fig_total_sales = px.scatter(
                plat_sum_df, x="Year", title="Vendas de Consoles da mesma desenvolvedora",
                y='Units',
                labels={'Units': 'Unidades vendidas', 'Name': 'Console', 'Year': 'Ano'},
                height=500,
                color='Name',
                color_discrete_map=discrete_colors,
                )
            
            fig_total_sales.update_layout(
                title=dict(font=dict(size=20)),
                # yaxis=dict(tickformat=".2f", ticksuffix='Mi', tickprefix='$'),
                # yaxis=dict(tickformat=".2f", ticksuffix='Mi'),
                
            )

            fig_total_sales.update_layout(
                xaxis=dict(title=None, fixedrange=True),
                
                yaxis=dict(title=None, fixedrange=True),
                legend=dict(
                title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"
                )
            )

            fig_total_sales.update_yaxes(
                showgrid=False, 
                color='black'
            )
            fig_total_sales.update_traces(marker=dict(size=6,
                                    line=dict(width=0.8, 
                                            color='DarkSlateGrey')),
                        selector=dict(mode='markers'))
            
            st.plotly_chart(fig_total_sales, use_container_width=True,)

# Assuming game_df is already defined and contains your game data
with st.expander("Jogos disponíveis", icon=":material/stadia_controller:"):
    game_df['year'] = game_df["year"].astype('string')
    game_df['year'] = game_df['year'].fillna("Indefinido")

    top_menu = st.columns(3)
    inp = st.columns([0.3, 0.3, 0.3])
    
    with top_menu[0]:
        sort = st.radio("Sort Data", options=["Yes", "No"], index=1)  # Default to "No"
    
    if sort == "Yes":
        with top_menu[1]:
            with inp[0]:
                sort_field = st.selectbox("Sort By", options=game_df.columns)
            with inp[1]:
                filter_year = st.selectbox("Ano", options= ["All"] + game_df['year'].drop_duplicates().to_list(),
                                        index=0, key="year_filter")
            with inp[2]:
                name_filter = st.text_input(
                    "Nome do Jogo", 
                )

        with top_menu[2]:
            sort_direction = st.radio(
                "Direction", options=["⬆️ Ascending", "⬇️ Descending"], horizontal=True
            )
        
        # Sort the DataFrame based on user input
        # if filter_year != "All" or name_filter != "":
        #     game_df = game_df.loc[(game_df['year'] == filter_year) & (game_df['name'].str.contains(name_filter)) ].sort_values(
        #         by=sort_field, ascending=(sort_direction == "⬆️ Ascending"), ignore_index=True
        #     )
        if name_filter != "": 
            game_df = game_df.loc[(game_df['name'].str.contains(name_filter))].sort_values(
                by=sort_field, ascending=(sort_direction == "⬆️ Ascending"), ignore_index=True
            )
        else:
            game_df = game_df.sort_values(
                by=sort_field, ascending=(sort_direction == "⬆️ Ascending"), ignore_index=True
            )

    pagination = st.container()

    bottom_menu = st.columns((4, 1, 1))
    
    with bottom_menu[2]:
        batch_size = st.selectbox("Page Size", options=[25, 50, 100], index=0)  # Default to 25
    
    with bottom_menu[1]:
        total_pages = (len(game_df) // batch_size) + (1 if len(game_df) % batch_size > 0 else 0)
        
        current_page = st.number_input(
            "Page", min_value=1, max_value=total_pages, step=1, value=1  # Default to page 1
        )
    
    with bottom_menu[0]:
        st.markdown(f"Page **{current_page}** of **{total_pages}** ")

    # Calculate the start and end indices for pagination
    start_idx = (current_page - 1) * batch_size
    end_idx = start_idx + batch_size

    # Display the paginated DataFrame
    st.data_editor(
        game_df.iloc[start_idx:end_idx],  # Show only the current page's data
        column_config={
            "game_image": st.column_config.ImageColumn("Imagem"),
            "name": "Nome do jogo",
            "url": st.column_config.LinkColumn(
                "Nome do Jogo", 
                validate=r"^https://[a-z]+\.uvlist\.net/game-\d+-[A-Za-z\.\+]+$",
                display_text=r"https://[a-z]+\.uvlist\.net/game-\d+-([^-\n]+)"  # Captures everything before the last "-"
            ),
            "publisher": "Publicadora",
            "developer": "Desenvolvedora",
            "year": "Ano",
        },
        disabled=True,
        column_order=["game_image", "url", "publisher", 'developer', 'year'],
        hide_index=True,
    )
