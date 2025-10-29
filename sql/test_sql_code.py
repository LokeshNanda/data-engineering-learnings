import duckdb

# Update this with your sql file
SQL_FILE = '.\sql\\17-BusinessExpansion.sql'

# Database file name
DB_FILE = '.\duck_db\sql_challenges.duckdb'

try:
    # 1. Read the SQL code from the file
    with open(SQL_FILE, 'r') as f:
        sql_query = f.read()

    # 2. Connect to the DuckDB file
    conn = duckdb.connect(database=DB_FILE)

    # 3. Execute the SQL query
    result = conn.sql(sql_query).to_df()

    # 4. Print the result
    print(f"--- Results from {SQL_FILE} ---")
    print(result.to_markdown(index=False))

    conn.close()

except Exception as e:
    print(f"An error occurred while running the query: {e}")