import duckdb
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, collect_list, concat_ws

spark = SparkSession.builder.appName("DataFrameCreation").getOrCreate()
con = duckdb.connect(database='.\duck_db\sql_challenges.duckdb', read_only=False)

users_pandas_df = con.execute("SELECT * FROM users_phone;").fetchdf()
phones_pandas_df = con.execute("SELECT * FROM phones;").fetchdf()


users_df = spark.createDataFrame(users_pandas_df)
phones_df = spark.createDataFrame(phones_pandas_df)

# Add a constant KEY column for merging
users_df = users_df.withColumn('KEY', expr('1'))
phones_df = phones_df.withColumn('KEY', expr('1'))

# Perform outer join on the KEY column
merged_df = users_df.join(phones_df, on='KEY', how='outer')

# Filter based on conditions
final_df = merged_df.filter(
    (col('savings') >= col('cost') * 0.2) &
    (col('monthly_salary') * 0.2 >= col('cost') * (0.8 / 6))
).groupBy('user_name') \
 .agg(collect_list('phone_name').alias('phone_names')) \
 .select('user_name', concat_ws(',', 'phone_names').alias('phone_name'))

# Show the final result
final_df.show(truncate=False)

spark.stop()
