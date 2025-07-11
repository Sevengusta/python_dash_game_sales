# Data Source
- Source: The data was obtained through Web scraping from many game data information (vgchartz, uvlist, opencritic etc).
- All the data was stored in Google Cloud BigQuery for make ETL Transformations.

# Features
- Games: information about sales of games with more than 66.000 around the world.
- Platforms: information about platform sales, and games released by platform. More than 164.000 games
- Generatons: Major informations about generations of games.


# Modificações realizadas no dataset
- **Data Cleaning**: Rows with missing information about the games were removed.
- **Exclusion of Irrelevant Years**: Data from the most recent years (2017-2020) were considered irrelevant and not used.
- **New Column Global_Sales**: A new column called Global_Sales was created, containing the sum of sales in the four available regions (North America, Europe, Japan, and other regions).
 
The project is available at:: https://sevengusta-dash-game-sales.streamlit.app/
