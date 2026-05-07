# from pyspark.sql import SparkSession
import os
from pyspark.sql import SparkSession
from pyspark.pandas import read_parquet
os.environ["PYARROW_IGNORE_TIMEZONE"] = "1" 
spark = SparkSession.builder.appName("MyApp").master("local[*]") \
     .config("spark.driver.memory", "8g") \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.maxResultSize", "1g") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.sql.shuffle.partitions", "8") \
    .config("spark.default.parallelism", "8") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .config("spark.sql.files.maxPartitionBytes", "64m") \
    .config("spark.sql.files.openCostInBytes", "4194304") \
    .getOrCreate()
df = spark.read.parquet('./food.parquet')


df_single = df.select("with_sweeteners").dropna()
print(f'Hello count: {df_single.count()}')
from pyspark.ml.clustering import KMeans


from pyspark.ml.feature import VectorAssembler

assembler = VectorAssembler(
    inputCols=["with_sweeteners"],
    outputCol="features"
)

df2 = assembler.transform(df.fillna(0, subset=["with_sweeteners"]))
kmeans = KMeans(featuresCol='features',k=2)
model = kmeans.fit(df2)
predictions = model.transform(df2)

centers = model.clusterCenters()
print("Cluster Centers: ")
for center in centers:
    print(center)

print(spark)
spark.stop()