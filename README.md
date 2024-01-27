# Data Source
- Source: The data was obtained through scraping from the vgchartz website.
- Size: Over 16,500 rows and 11 columns.
# Column Details
- rank: Index of the column
- Name: Name of the game
- Platform: Platform the game was released on
- Year: Year of its publication
- Genre: Genre assigned to the game
- Publisher: Game publisher
- NA_Sales: Sales in North America
- EU_Sales: Sales in Europe
- JP_Sales: Sales in Japan
- Other_Sales: Sales in other regions



Project data source: https://www.kaggle.com/datasets/gregorut/videogamesales/code?datasetId=284&sortBy=voteCount 
# Modificações realizadas no dataset
- **Data Cleaning**: Rows with missing information about the games were removed.
- **Exclusion of Irrelevant Years**: Data from the most recent years (2017-2020) were considered irrelevant and not used.
- **New Column Global_Sales**: A new column called Global_Sales was created, containing the sum of sales in the four available regions (North America, Europe, Japan, and other regions).
 
The project is available at:: https://sevengusta-dash-game-sales.streamlit.app/
