import duckdb
from typing import Dict, List, Tuple, Any
import os
import json

# Define the database file name
DB_FILE = '.\duck_db\sql_challenges.duckdb'
DATA_FILE = '.\duck_db\data\\tables.json'

def load_table_data(file_path: str) -> list:
    """Loads the table definitions and data from a JSON file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")
        
    with open(file_path, 'r') as f:
        # The JSON file is expected to be a list of table objects
        return json.load(f)

def create_and_populate_duckdb(db_file: str, tables_list: list):
    """
    Creates or connects to a DuckDB file and populates it with data from the loaded list.
    """
    try:
        conn = duckdb.connect(database=db_file)
        print(f"Connected to DuckDB file: {db_file}")

        for table_info in tables_list:
            table_name = table_info['table_name']
            schema = table_info['schema']
            data = table_info['data']
            
            # 1. Construct the CREATE TABLE statement
            column_definitions = ", ".join(
                [f"{col['column_name']} {col['data_type']}" for col in schema]
            )
            create_sql = f"CREATE OR REPLACE TABLE {table_name} ({column_definitions});"
            
            # 2. Execute CREATE TABLE
            conn.execute(create_sql)
            print(f"Created table: {table_name}")
            
            # 3. Insert Data
            if data:
                placeholders = ", ".join(['?' for _ in schema])
                insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders});"
                # The data list (list of lists) is perfect for executemany
                conn.executemany(insert_sql, data)
                print(f"Inserted {len(data)} rows into {table_name}.")
            else:
                print(f"No data to insert for {table_name}.")

        conn.commit()
        conn.close()
        print("\nSuccessfully populated the DuckDB file.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    try:
        # Load the data from the JSON file
        data_to_populate = load_table_data(DATA_FILE)
    
        # Run the population process
        create_and_populate_duckdb(DB_FILE, data_to_populate)

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading data: {e}")
    except Exception as e:
        print(f"A general error occurred: {e}")