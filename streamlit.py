import streamlit as st
import time
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Union
import pandas as pd

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

# ========== Styles ============ #
colors = [
    '#3366CC', '#DC3912', '#FF9900', '#109618', '#990099',
    '#0099C6', '#DD4477', '#66AA00', '#B82E2E', '#316395'
]  # px.colors.qualitative.G10

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
# make containers
header = st.container()
data_sets = st.container()
features = st.container()

# ========== Figures Layout ============ #
ind1, ind2, ind3 = st.columns(3)
v_bar1, v_bar2 = st.columns(2)
scatter, *args = st.columns(1)
frame1, *args = st.columns(1)
h_bar, *args = st.columns(1)
frame2, *args = st.columns(1)


# ========== Tratamento inicial do df ============ #
df = pd.read_csv('vgsales.csv')

df.dropna(inplace=True)
df.drop('Rank', axis=1, inplace=True)

df['Year'] = pd.to_datetime(df['Year'], format='%Y').dt.year
df = df.sort_values(by='Year', ascending=True)
df = df[df['Year'] < 2017]

df['Year'] = df['Year'].astype('int')
df['Other_Sales'] = df['Other_Sales'].astype('float')
df['Global_Sales'] = df['Global_Sales'].astype('float')
df['JP_Sales'] = df['JP_Sales'].astype('float')
df['EU_Sales'] = df['EU_Sales'].astype('float')
df['NA_Sales'] = df['NA_Sales'].astype('float')

#  ---- facilties to data mapping
global_genres = [
    'Adventure', 'Action', 'Racing', 'Sports', 'Strategy', 'Fighting',
    'Misc', 'Platform', 'Puzzle', 'Role-Playing', 'Simulation', 'Shooter'
]
genres_PT = [
    'Ação', 'Aventura', 'Luta', 'Miscelânea', 'Plataforma', 'Puzzle',
    'Corrida', 'Role-Playing', 'Tiro', 'Simulação', 'Esportes', 'Estratégia'
]
regions = [ 'EU_Sales', 'JP_Sales',  'NA_Sales', 'Other_Sales']
regions_PT = [ 'Europa', 'Japão', 'América do Norte', 'Outras Regiões']

legend_data = {
        'NA_Sales': 'América do Norte',
        'EU_Sales': 'Europa',
        'JP_Sales': 'Japão',
        'Other_Sales': 'Outros'
    }

genres_PT = sorted(genres_PT)


# ---- features que serão utilizadas para filtrar os dados
with features:
    def filter_update():
        if all(not st.session_state[str(i)] for i in range(1, 12)):
            st.session_state['0'] = True

        conditions = {
            0: 1983,
            2: 1981,
            4: 1991,
            7: 1981,
            8: 1981,
            9: 1986,
            10: 1981
        }
        # Loop through the dictionary and update 'min' based on conditions
        for key, value in conditions.items():
            if all(not st.session_state[str(i)] for i in range(12) if i != key) and st.session_state.max < value:
                st.session_state.min = value
                break  # Exit the loop after the first condition is met

        if st.session_state.on:
            for index in range(0, 12):
                st.session_state[str(index)] = True
        if st.session_state.off:
            for index in range(0, 12):
                st.session_state[str(index)] = False
            st.session_state['0'] = True

        if st.session_state.min > st.session_state.max:
            st.session_state.max = st.session_state.min

    st.sidebar.write('Filtro por gêneros')
    on = st.sidebar.button(
        'Selecionar tudo',
        key='on',
        on_click=filter_update
    )
    off = st.sidebar.button(
        'Limpar seleções',
        key='off',
        on_click=filter_update
    )
    selected_filter = [
        st.sidebar.checkbox(
            value=True,
            label=genres_PT[index],
            key=index,
            on_change=filter_update
        )
        for index, genre in enumerate(global_genres)]

    inicial_year = (year for year in range(1980, 2017))
    final_year = sorted((year for year in range(1980, 2017)), reverse=True)

    min = st.sidebar.selectbox(
        'Ano inicial',
        on_change=filter_update,
        key='min',
        options=(inicial_year)
    )
    max = st.sidebar.selectbox(
        'Ano final',
        on_change=filter_update,
        key='max',
        options=(final_year)
    )

selected_filter = []
for index, genre in enumerate(global_genres):
    if st.session_state[index]:
        selected_filter.append(genre)
df_filtered = df[df['Genre'].isin(selected_filter) == True]


# ---- order df by  global sales
df_global = df_filtered.sort_values(by='Global_Sales', ascending=False)

# Função que cria um fábrica de dfs, para realizar amostragens.
# faz o recalculo dos dfs, toda vez que a filtro é mudada!


def df_factory(min, max, column: Union[str, List[str]], selected_column: Union[str, List[str]] = 'Global_Sales'):
    if min:
        _df = df_global[(df_global['Year'] >= min) &
                        (df_global['Year'] <= max)]
        _df = _df.groupby(column)[selected_column].sum().reset_index()
        _df = _df.sort_values(by=selected_column, ascending=False)
        return _df
    else:
        return df_global



with header:
    st.title(":blue[Mercado de jogos eletrônicos]")

with data_sets:
    df_name = df_factory(min, max, 'Name')
    best_game = df_name['Name'].iloc[0]
    sales = df_name[df_name['Name'] ==
                    best_game]['Global_Sales'].sum() * 1000000
    fig_global_sales = go.Figure(go.Indicator(
        mode="number",
        title={"text": f"<span style='font-size:100%; color: #3366CC; text-align:center;font-weight:bold'>Título mais vendido</span><br><span style='font-size:80%; color: #3366CC; font-weight:bold'> {best_game} </span><br><span style='font-size:70%; color:#000';>Em US$</span>"},
        value=sales,
        number={'prefix': '$', 'font' :{'color': '#3366CC'}},
        domain={'x': [0, 1], 'y': [0, 1]},
    ))
    fig_global_sales.update_layout(height=270)
    ind1.plotly_chart(fig_global_sales, use_container_width=True, )

with data_sets:
    df_count_games = df_factory(min, max, 'Name')
    fig_total_games = go.Figure(go.Indicator(
        mode='number',
        title={"text": f"<span style='font-size:100%; color: #DC3912;  font-weight:bold'>Foram produzidos <br> </span><br><span style='font-size:80%; color:#000'>Em títulos</span>"},
        number={'valueformat': '.0f', 'font' :{'color': '#DC3912'}},
        value=df_count_games['Name'].count(),
        domain={'x': [0, 1], 'y': [0, 1]},
    ))
    fig_total_games.update_layout(height=270)
    ind2.plotly_chart(fig_total_games, use_container_width=True)

with data_sets:
    df_pub = df_factory(min, max, 'Publisher')
    best_pub = df_pub['Publisher'].iloc[0]
    sales = df_pub[df_pub['Publisher'] ==
                   best_pub]['Global_Sales'].sum() * 1000000
    fig_total_games = go.Figure(go.Indicator(
        mode='number',
        title={"text": f"<span style='font-size:100%; color: #FF9900; text-align:center;font-weight:bold'>Maior Desenvolvedora</span><br><span style='font-size:80%;  color: #FF9900; font-weight:bold'> {best_pub}</span><br><span style='font-size:70%; color:#000'>Em US$</span>"},
        value=sales,
        number={'prefix': '$',  'font' :{'color': '#FF9900'}},
        domain={'x': [0, 1], 'y': [0, 1]},
    ))
    fig_total_games.update_layout(height=270)
    ind3.plotly_chart(fig_total_games, use_container_width=True)


with data_sets:

    df_plat = df_factory(min, max, 'Platform').round(2).head(10)
    df_plat = df_plat.sort_values(by='Global_Sales', ascending=True)
    text_top_plat = [
        f'{x} - US${y} milhões'
        for x, y in zip(df_plat['Platform'].unique(),
                        df_plat['Global_Sales'])]

    fig_top_plat = px.bar(
        hover_data=None,
        hover_name=None,
        x=df_plat['Global_Sales'],
        y=df_plat['Platform'],
        orientation='h', text=text_top_plat,
        title='Maiores Plataformas em faturamento no mundo'
    )
    fig_top_plat.update_traces(marker=dict(color=colors, coloraxis="coloraxis"),)
    fig_top_plat.update_layout(
        main_config,
        font_color='black',
        hovermode=False,
        xaxis=dict(fixedrange=True, visible=False),
        yaxis=dict(visible=False),
    )

    v_bar1.plotly_chart(
        fig_top_plat,
        use_container_width=True,
    )

with data_sets:
    df_pub = df_factory(min, max, 'Publisher').round(2).head(10)
    df_pub = df_pub.sort_values(by='Global_Sales', ascending=True)

    text_top_games = [
        f' {x} - US${y} milhões'
        for x, y in zip(df_pub['Publisher'].unique(), df_pub['Global_Sales'])
    ]

    fig_top_games = go.Figure(go.Bar(
        x=df_pub['Global_Sales'],
        y=df_pub['Publisher'],
        orientation='h', text=text_top_games
    ))
    fig_top_games.update_traces(marker=dict(color=colors, coloraxis="coloraxis"),)

    fig_top_games.update_layout(
        main_config,
        font_color='black',
        hovermode=False, 
        xaxis=dict(fixedrange=True, visible=False),
        yaxis=dict(visible=False),
        title='Maiores Desenvolvedoras em faturamento no mundo'
    )
    v_bar2.plotly_chart(fig_top_games, use_container_width=True)

with data_sets:
    global_regions = regions.copy()
    global_regions.append('Global_Sales')
    df_region = df_factory(min, max, 'Year', global_regions)

    df_region = df_region.sort_values(by='Year', ascending=False)

    fig_sales_region = px.line(
        df_region, x="Year", title="Faturamento por região",
        y=regions,
        labels={'variable': 'Região', 'value': 'Vendas', 'Year': 'Ano'},
        height=500,
        color_discrete_sequence=colors,
    )
    fig_sales_region.update_layout(
        yaxis=dict(tickformat=".2f", ticksuffix='Mi', tickprefix='$'),
        
    )

    fig_sales_region.add_trace(go.Scatter(
        x=df_region['Year'], y=df_region['Global_Sales'], mode='lines+markers',
        fill='tonexty', fillcolor='rgba(255,0,0,0.2)', name='Total',
        textposition='top left',

    ))

    fig_sales_region.update_layout(
        xaxis=dict(title=None, fixedrange=True),
        font_color='black',
        yaxis=dict(title=None, fixedrange=True),
        legend=dict(
        title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"
        )
    )

    _regions_PT = regions_PT.copy()
    for index, _regions_PT in enumerate(_regions_PT):
        fig_sales_region.update_traces(
            name=_regions_PT,
            selector=dict(name=regions[index])
        )
    fig_sales_region.update_xaxes(
        tickfont=dict(color='black'),
    )
    fig_sales_region.update_yaxes(
        showgrid=False, 
        tickfont=dict(color='black'),
        color='black'
    )
    scatter.plotly_chart(fig_sales_region, use_container_width=True,)

with data_sets:
    df_NA = df_factory(min, max, 'Name', 'NA_Sales').round(2).head(5)
    df_EU = df_factory(min, max, 'Name', 'EU_Sales').round(2).head(5)
    df_JP = df_factory(min, max, 'Name', 'JP_Sales').round(2).head(5)
    df_Other = df_factory(min, max, 'Name', 'Other_Sales').round(2).head(5)

    fig = make_subplots(
        shared_yaxes=True,
        rows=1, cols=4,
        specs=[[{"type": "bar"}, {"type": "bar"},
                {"type": "bar"}, {"type": "bar"}]],
    )
    fig.add_trace(go.Bar(
        y=df_NA['NA_Sales'], x=df_NA['Name'], marker=dict(color=colors[2], coloraxis="coloraxis"),
        name='América do Norte', text=[f'{x:.1f}Mi' for x in df_NA['NA_Sales']],
    ), row=1, col=4)
    fig.add_trace(go.Bar(
        y=df_EU['EU_Sales'], x=df_EU['Name'], marker=dict(color=colors[0], coloraxis="coloraxis"),
        name='Europa', text=[f'{x:.1f}Mi' for x in df_EU['EU_Sales']],

    ), row=1, col=1)
    fig.add_trace(go.Bar(
        y=df_JP['JP_Sales'], x=df_JP['Name'], marker=dict(color=colors[1], coloraxis="coloraxis"),
        name='Japão', text=[f'{x:.1f}Mi' for x in df_JP['JP_Sales']],
    ), row=1, col=2)
    
    fig.add_trace(go.Bar(
        y=df_Other['Other_Sales'], x=df_Other['Name'], marker=dict(color=colors[3], coloraxis="coloraxis"),
        name='Outras Regiões',
        text=[f'{x:.1f}Mi' for x in df_Other['Other_Sales']],
    ), row=1, col=3)
    for i in range(1, 5):
        fig.update_xaxes(row=1, col=i, visible=False, fixedrange=True,)
        fig.update_yaxes(row=1, col=i, visible=False, fixedrange=True)
        fig.update_layout(
            showlegend=True,
            legend=dict(
            title=None ,orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"
            )
        )
        fig.update_traces( 
            row=1, col=i, textfont_size=12, textangle=0,
            textposition="outside", cliponaxis=False,
        )

    fig.update_layout(title_text='Títulos mais vendidos em cada Região', font_color='black',)
    frame1.plotly_chart(fig, use_container_width=True, height=400, )

with data_sets:
    df_genre = df_factory(min, max, 'Genre', regions)

    genre = px.bar(
        df_genre,
        y='Genre',
        x=regions,
        title='Vendas por Gênero',
        labels={'variable': 'Região', 'value':'Vendas', 'Genre': 'Gênero' },
        orientation='h',
        color_discrete_sequence=colors,
        
    )
    genre.update_xaxes(
        fixedrange=True,
        showgrid=False,
        visible=False
    )
    genre.update_yaxes(
        ticktext=genres_PT, 
        tickfont=dict(color='black'),
        tickvals=global_genres,  categoryorder='total ascending',)
    genre.update_layout(
        font_color='black',
        hovermode=None,
        height=700,
        xaxis=dict(fixedrange=True),
        yaxis_title=None,
        xaxis_title=None,
        legend=dict(
        title=None,orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"
        )
    )
    
    for index, region in enumerate(regions):
        genre.update_traces(
            text=[f'{x:.2f}Mi' for x in df_genre[region].round(2)],
            name=regions_PT[index],
            selector=dict(name=region)
        )
    genre.update_traces(
        textangle=0,
        textposition="outside", 
    )

    frame2.plotly_chart(genre, use_container_width=True )


st.markdown(
    "Fonte de dados do projeto: https://www.kaggle.com/datasets/gregorut/videogamesales")
