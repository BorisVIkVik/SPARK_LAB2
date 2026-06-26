# from pyspark.sql import SparkSession
import os
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
# from pyspark.pandas import read_parquet
os.environ["PYARROW_IGNORE_TIMEZONE"] = "1" 
spark = SparkSession.builder.appName("MyApp").master("local[*]") \
     .config("spark.driver.memory", "8g") \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.maxResultSize", "2g") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.sql.shuffle.partitions", "8") \
    .config("spark.default.parallelism", "8") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .config("spark.sql.files.maxPartitionBytes", "64m") \
    .config("spark.sql.files.openCostInBytes", "4194304") \
    .config("spark.hadoop.dfs.client.use.datanode.hostname", "true") \
    .config("spark.hadoop.dfs.datanode.use.datanode.hostname", "true") \
    .getOrCreate()
df = spark.read.parquet('hdfs://localhost:8020/test/food.parquet')


df_single = df.select("known_ingredients_n").dropna()
# del df
print(f'Hello count: {df_single.count()}')
# del df_single

assembler = VectorAssembler(
    inputCols=["known_ingredients_n"],
    outputCol="features"
)

df2 = assembler.transform(df.fillna(0, subset=["known_ingredients_n"]))
# del df
kmeans = KMeans(featuresCol='features',k=2)
model = kmeans.fit(df2)
predictions = model.transform(df2)

centers = model.clusterCenters()
print("Cluster Centers: ")
for center in centers:
    print(center)
df = spark.createDataFrame([center.tolist() for center in centers])
df.write.mode("overwrite").csv("hdfs://localhost:8020/test/output.csv")
print(spark)
spark.stop()