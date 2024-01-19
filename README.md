# Fonte de dados
- Origem: Os dados foram obtidos através de scraping do site [vgchartz](https://vgchartz.com./).
- Tamanho: Mais de 16.500 linhas e 11 colunas.
# Detalhamento das colunas
- **rank**: Índice da coluna
- **Name**: Nome do jogo
- **Plataform**: Plataforma que o jogo foi lançado
- **Year**: Ano de sua publicação
- **Genre**: Gênero atribuído ao jogo
- **Publisher**: Distribuidora dos jogos
- **NA_Sales**: Vendas na América do Norte
- **EU_Sales**: Vendas na Europa
- **JP_Sales**: Vendas no Japão
- **Other_Sales**: Vendas em outras regiões



fonte de dados do projeto: https://www.kaggle.com/datasets/gregorut/videogamesales/code?datasetId=284&sortBy=voteCount 
# Modificações realizadas no dataset
- **Limpeza de Dados**: Linhas com informações ausentes sobre os jogos foram removidas.
- **Exclusão de Anos Irrelevantes**: Dados dos anos mais recentes (2017-2020) foram considerados irrelevantes e não foram utilizados.
- **Nova Coluna Global_Sales**: Foi criada uma coluna chamada Global_Sales, que contém a soma das vendas nas quatro regiões disponíveis (América do Norte, Europa, Japão e outras regiões).
 
O projeto está disponível em: https://sevengusta-dash-game-sales.streamlit.app/
