'''
Amazon is expanding their pharmacy business to new cities every year. 
You are given a table of business operations where you have information about cities where Amazon is doing operations along with the business date information.
Write a SQL to find year wise number of new cities added to the business, display the output in increasing order of year. 

Table: business_operations
+---------------+-----------+
| COLUMN_NAME   | DATA_TYPE |
+---------------+-----------+
| business_date | date      |
| city_id       | int       |
+---------------+-----------+

select * from business_operations ;

-- OUTPUT:
+----------------------+------------------+
| first_operation_year | no_of_new_cities |
+----------------------+------------------+
|                 2020 |                2 |
|                 2021 |                1 |
|                 2022 |                1 |
+----------------------+------------------+
'''
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, DateType, IntegerType
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("DataFrameCreation").getOrCreate()
schema = StructType([
    StructField("business_date", DateType(), True),
    StructField("city_id", IntegerType(), True)
])

data = [
    ("2020-01-02", 3),
    ("2020-07-01", 7),
    ("2021-01-01", 3),
    ("2021-02-03", 19),
    ("2022-12-01", 3),
    ("2022-12-15", 3),
    ("2022-02-28", 12)
]

business_operations_df = spark.createDataFrame(data, ["business_date", "city_id"])

business_operations_df = business_operations_df.withColumn("business_date", F.to_date("business_date"))
fr_op_year_df = business_operations_df.withColumn("first_operation_year", F.year("business_date")).groupby("city_id").agg(F.min("first_operation_year").alias("first_operation_year"))
final_df = fr_op_year_df.groupby("first_operation_year").agg(F.count("city_id").alias("no_of_new_cities")).sort("first_operation_year")
final_df.show()
