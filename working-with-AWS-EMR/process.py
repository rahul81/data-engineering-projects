
import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F, types as T



spark = SparkSession.builder.appName('Stock-SMA').getOrCreate()


input_path = sys.argv[1]
static_data_path = sys.argv[3]
output_path = sys.argv[2]


# create streaming data frame from input csv file 

schema = T.StructType([
    T.StructField("Date", T.StringType(), True),
    T.StructField("Open", T.DoubleType(), True),
    T.StructField("High", T.DoubleType(), True),
    T.StructField("Low", T.DoubleType(), True),
    T.StructField("Close", T.DoubleType(), True),
    T.StructField("Volume", T.DoubleType(), True),
    T.StructField("Name", T.StringType(), True)
])

df = (spark
             .read
             .csv(input_path, schema=schema,header=True))


company_df = spark.read.csv(static_data_path, inferSchema=True, header=True)

casted_df = (df.withColumn('timestamp', F.col('Date').cast('timestamp')))


windowed_df = (casted_df
               .groupby(F.window('timestamp', '5 days', '2 days'),'Name')
               .agg(F.mean('Close').alias('SMA_5')))

# perform a join operation on data stream
# join static data from csv file to data stream


# this will keep Company name null if it is not present in static data
joined_df = windowed_df.join(company_df, 'Name', 'left_outer') 


final_df = joined_df.select('window.start','window.end', 'Name', 'Company','SMA_5')


(final_df.write
    .format('csv')
    .mode('overwrite')
    .option('header',True)
    .save(output_path))