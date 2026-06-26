# from pyspark.sql import SparkSession
import os
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
import yaml

with open('config/spark_config.yaml') as f:
    cfg = yaml.safe_load(f)

os.environ["PYARROW_IGNORE_TIMEZONE"] = "1" 
builder = SparkSession.builder.appName(cfg['spark']['app_name']).master(cfg['spark']['master'])
    

for key, value in cfg['spark']['configs'].items():
    builder = builder.config(key, value)


spark = builder.getOrCreate()

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