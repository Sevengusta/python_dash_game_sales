from google.cloud import bigquery
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# set a connection with the database
conn = sqlite3.connect('../data/games_data.db')
c = conn.cursor()

def list_datasets(client_name):
    data_summary = []  # Initialize the list to store views information
    datasets = client_name.list_datasets()

    if datasets:
        for dataset in datasets:
            dataset_id = dataset.dataset_id
            dataset_ref = client_name.dataset(dataset_id)

            tables = client_name.list_tables(dataset_ref)
            for table in tables:
                table_info = {
                    "dataset_id": dataset_id,
                    "table_id": table.table_id,
                    "type": table.table_type
                }
                data_summary.append(table_info)
        return  data_summary
    else:
        logger.info(f"Nenhum dataset encontrado no projeto {client_name.project}.")
        return []
    
project_name = "python-dash-game-sales-pd"
client = bigquery.Client(project=project_name)
sources = list_datasets(client)

try: 
    for source in sources:
        if source['dataset_id'] == "final_data" or source['table_id'] == "platform_id":
            print(source)
            query = f'SELECT * FROM `{project_name}.{source['dataset_id']}.{source['table_id']}`'
            df = client.query(query).to_dataframe()
            df.to_csv(f"../data/{source['table_id']}.csv", index=False)
            columns = df.columns
                        # Create table with specified column types (assuming TEXT for all columns)
            columns = ', '.join([f"{col}" for col in columns])
            logger.info(columns)

            c.execute(f'''CREATE TABLE IF NOT EXISTS {source['table_id']} ({columns})''')
            df.to_sql(source['table_id'], conn, if_exists='replace', index=False)
    logger.info("Todos os dados foram salvos com sucesso")
finally:
    conn.close()