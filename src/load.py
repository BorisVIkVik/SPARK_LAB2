import os
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler

from hdfs import InsecureClient

client = InsecureClient('http://localhost:9870', user='root')
client.makedirs('/test')
client.set_permission('/test', '777')

import yaml

with open('config/spark_config.yaml') as f:
    cfg = yaml.safe_load(f)

os.environ["PYARROW_IGNORE_TIMEZONE"] = "1" 
builder = SparkSession.builder.appName(cfg['spark']['app_name']).master(cfg['spark']['master'])
    

for key, value in cfg['spark']['configs'].items():
    builder = builder.config(key, value)


spark = builder.getOrCreate()
df = spark.read.parquet('data/food.parquet').limit(1000)


df.write.mode("overwrite").parquet("hdfs://localhost:8020/test/food.parquet")
print(spark)
spark.stop()