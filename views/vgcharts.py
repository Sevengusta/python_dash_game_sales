import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sqlite3
conn = sqlite3.connect("data/games_data.db")


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
# make containers
header = st.container()
data_sets = st.container()
features = st.container()

# ========== Figures Layout ============ #
ind1, ind2, ind3 = st.columns([0.2,0.6,0.2])
v_bar1, v_bar2 = st.columns(2)
scatter, *args = st.columns(1)
frame1, *args = st.columns(1)
h_bar, *args = st.columns(1)
frame2, *args = st.columns(1)


@st.cache_data
def get_data(_conn):
    # ========== Tratamento inicial do df ============ #
    df = pd.read_sql(f"SELECT * FROM sales_game_data_v", _conn)
    conn.close()
    return df 

# ---- features que serão utilizadas para filtrar os dados
def filter_update():
    if st.session_state.min > st.session_state.max:
        st.session_state.max = st.session_state.min

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">',
                unsafe_allow_html=True)


        
# Função que cria um fábrica de dfs, para realizar amostragens.
# faz o recalculo dos dfs, toda vez que o filtro é mudado!

def df_factory(df, column, selected_column= 'Total_Sales', ):
        _df = df.groupby(column)[selected_column].sum().reset_index()
        _df = _df.sort_values(by=selected_column, ascending=False)
        return _df

def main():
    remote_css("https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css")
    df_global = df.sort_values(by='Total_Sales', ascending=False)

    with header:
        st.header(f"Mercado de jogos eletrônicos")
        st.markdown("<b>Considerações preliminares</b>", unsafe_allow_html=True)
        st.markdown("""Essa página contém dados sobre os jogos que informações sobre as suas vendas no site 
                    vgcharts [vgcharts](https://example.com).
                    """, unsafe_allow_html=True)

    with data_sets:

        df_count_games = df_global
        fig_total_games = go.Figure(go.Indicator(
            mode='number',
            title={"text": f"<span style='font-size:100%;  font-weight:bold'>Foram produzidos  </span><br><span style='font-size:75%'>Em títulos</span> <span style='font-size:70%';>Entre {min} e {max} <br></span>"},
            number={'valueformat': '.0f' if int(df_count_games['Name'].count()) < 1000 else '.3s'},
            value=int(df_count_games['Name'].count()),
            domain={'x': [0, 1], 'y': [0, 1]},
        ))
        fig_total_games.update_layout(height=270)
        ind2.plotly_chart(fig_total_games, use_container_width=True)

    with data_sets:

        df_plat = df_factory(df, 'Developer').round(2).head(10)
        df_plat = df_plat.sort_values(by='Total_Sales', ascending=True)
        text_top_plat = [
            f'{x} - {y} milhões'
            for x, y in zip(df_plat['Developer'].unique(),
                            df_plat['Total_Sales'])]

        fig_top_plat = px.bar(
            hover_data=None,
            hover_name=None,
            x=df_plat['Total_Sales'],
            y=df_plat['Developer'],
            orientation='h', text=text_top_plat,
            title='Maiores Desenvolvedoras em vendas no mundo'
        )
        fig_top_plat.update_traces(marker=dict(color=colors, coloraxis="coloraxis"))
        fig_top_plat.update_layout(
            main_config,
            hovermode=False,
            xaxis=dict(fixedrange=True, visible=False),
            yaxis=dict(visible=False),
        )

        v_bar1.plotly_chart(
            fig_top_plat,
            use_container_width=True,
        )

    with data_sets:

        df_pub = df_factory(df, 'Publisher').round(2).head(10)
        df_pub = df_pub.sort_values(by='Total_Sales', ascending=True)

        text_top_games = [
            f' {x} - {y} milhões'
            for x, y in zip(df_pub['Publisher'].unique(), df_pub['Total_Sales'])
        ]

        fig_top_games = go.Figure(go.Bar(
            x=df_pub['Total_Sales'],
            y=df_pub['Publisher'],
            orientation='h', text=text_top_games
        ))
        fig_top_games.update_traces(marker=dict(color=colors, coloraxis="coloraxis"),)

        fig_top_games.update_layout(
            main_config,
            
            hovermode=False, 
            xaxis=dict(fixedrange=True, visible=False),
            yaxis=dict(visible=False),
            title='Maiores Publicadoras em vendas no mundo'
        )
        v_bar2.plotly_chart(fig_top_games, use_container_width=True)

    with data_sets:
        df_total_sales_monthly = df_factory(df, "Period" ,'Total_Sales')
        df_total_sales_yearly = df_factory(df, "Year" ,'Total_Sales')
        
        if max - min > 5: 
            fig_total_sales = px.scatter(
                df_total_sales_yearly, x="Year", title="Vendas Totais do setor em milhões",
                y='Total_Sales',
                labels={'variable': 'Região', 'value': 'Vendas', 'Year': 'Ano'},
                height=500,

                color_discrete_sequence=["#ff7c04"],
            )
        else:
            fig_total_sales = px.scatter(
                df_total_sales_monthly, x="Period", title="Vendas Totais do setor em milhões",
                y='Total_Sales',
                labels={'variable': 'Região', 'value': 'Vendas', 'Year': 'Ano'},
                height=500,
                color_discrete_sequence=["#ff7c04"],
            )

        fig_total_sales.update_layout(
            title=dict(font=dict(size=20)),
            # yaxis=dict(tickformat=".2f", ticksuffix='Mi', tickprefix='$'),
            yaxis=dict(tickformat=".2f", ticksuffix='Mi'),
            
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
        scatter.plotly_chart(fig_total_sales, use_container_width=True,)

    with data_sets:
        df_name_games = df_factory(df.loc[(df['Platform'] != "Series") & (df['Platform'] != "All")]
                             , ['Name', 'Categoria', 'Platform', 'Period'], 'Total_Sales').round(2).head(10)
        fig = px.bar(
            df_name_games.head(10),
            color_discrete_map=discrete_colors,
            y='Total_Sales',
            x='Name',
            title='Vendas por Gênero',
            text_auto='.2f',
            labels={'Name': 'Nome do Jogo', 'Total_Sales':'Vendas', 
                    'Categoria': 'Gênero', "Platform": "Plataforma",
                     'Period': "Ano e Mês de Lançamento" },
            color="Categoria",
            hover_data={'Platform': True, "Period": True}

            
        )
        fig.update_xaxes(
            fixedrange=True,
            showgrid=False,
            visible=False
        )
        fig.update_yaxes(
            showgrid=False,
        )

        fig.update_layout(
            title=dict(font=dict(size=20)),
            title_text='Top 10 Títulos mais vendidos em milhões de vendas',
            hovermode=None,
            height=500,
            xaxis=dict(fixedrange=True, categoryorder='total ascending'),
            yaxis=dict(tickformat=".2f", ticksuffix='Mi'),
            yaxis_title=None,
            xaxis_title=None,
            legend=dict(
            title=None,orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center",
            )
        )


        frame1.plotly_chart(fig, use_container_width=True, height=400, )

    with data_sets:
        df_multi = df_factory(df.loc[(df['Platform'] == "Series") | (df['Platform'] == "All")]
                             , ['Name', 'Categoria', 'Platform' ,'Period'], 'Total_Sales').round(2).head(10)
        fig = px.bar(
            df_multi.head(10),
            color_discrete_map=discrete_colors,
            y='Total_Sales',
            x='Name',
            title='Vendas por Gênero',
            text_auto='.2f',
            labels={'Name': 'Nome do Jogo', 'Total_Sales':'Vendas',
                     'Categoria': 'Gênero', "Platform": "Plataforma",
                      "Period" :"Ano e Mês Lançamento" },
            color="Categoria",
            hover_data={'Platform': True, "Period": True}  # Add this line to show platform info on hover

            
        )
        fig.update_xaxes(
            fixedrange=True,
            showgrid=False,
            visible=False
        )
        fig.update_yaxes(
            showgrid=False,
        )

        fig.update_layout(
            title=dict(font=dict(size=20)),
            title_text='Top 10 Séries e Jogos Multi-Plataforma',
            hovermode=None,
            height=500,
            xaxis=dict(fixedrange=True, categoryorder='total ascending'),
            yaxis=dict(tickformat=".2f", ticksuffix='Mi'),
            yaxis_title=None,
            xaxis_title=None,
            legend=dict(
            title=None,orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center",
            )
        )


        frame1.plotly_chart(fig, use_container_width=True, height=400, )


    st.markdown("Fonte de dados do projeto: https://www.vgchartz.com/gamedb/")
    st.markdown("Fonte de dados do projeto: https://gamefaqs.gamespot.com/")

def do_filter(df, session):
    # Get the true categories based on the session filter
    if selected_filter:
        true_categories = [value for index, value in enumerate(selected_filter)]

        # Filter the DataFrame based on categories and year range
        df = df[
            (df['Categoria'].isin(true_categories)) & 
            (df['Year'] >= session['min']) & 
            (df['Year'] <= session['max'])
        ]
        return df
    else: 
            df = df[
                (df['Year'] >= session['min']) & 
                (df['Year'] <= session['max'])
            ]
    return df

if __name__ == "__main__":
    
    df = get_data(conn)
    categorias = sorted(df['Categoria'].drop_duplicates())
    discrete_colors = {categoria :colors[index] for index, categoria in enumerate(categorias)}
    # Initialize session state for filters
    if not  st.session_state:
        st.session_state.min = 1977
        st.session_state.max = 2025
    
    
    with features:
        selected_filter = st.sidebar.multiselect(
            "Filtro por gêneros",
            options=categorias,
        )
        

        inicial_year = (year for year in range(1977, 2026))
        final_year = sorted((year for year in range(1977, 2026)), reverse=True)

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
    
    df = do_filter(df,st.session_state)
    try:
        main()
    except:
        st.warning("⚠️ Nenhum jogo com essas características foi encontrado")