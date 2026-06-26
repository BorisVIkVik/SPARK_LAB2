import os
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler

from hdfs import InsecureClient

client = InsecureClient('http://localhost:9870', user='root')
client.makedirs('/test')
client.set_permission('/test', '777')

os.environ["PYARROW_IGNORE_TIMEZONE"] = "1" 
spark = SparkSession.builder.appName("MyApp").master("local[*]") \
     .config("spark.driver.memory", "8g") \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.maxResultSize", "2g") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.sql.shuffle.partitions", "16") \
    .config("spark.default.parallelism", "16") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .config("spark.sql.files.maxPartitionBytes", "256m") \
    .config("spark.sql.files.openCostInBytes", "4194304") \
    .config("spark.hadoop.dfs.client.use.datanode.hostname", "true") \
    .config("spark.hadoop.dfs.datanode.use.datanode.hostname", "true") \
    .getOrCreate()
df = spark.read.parquet('data/food.parquet').limit(1000)


df.write.mode("overwrite").parquet("hdfs://localhost:8020/test/food.parquet")
print(spark)
spark.stop()