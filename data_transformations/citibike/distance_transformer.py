# data_transformations/citibike/distance_transformer.py
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType

METERS_PER_FOOT = 0.3048
FEET_PER_MILE = 5280
EARTH_RADIUS_IN_METERS = 6371e3
METERS_PER_MILE = METERS_PER_FOOT * FEET_PER_MILE

def compute_distance(_spark: SparkSession, dataframe: DataFrame) -> DataFrame:
    lat1 = F.radians(F.col("start_station_latitude"))
    lon1 = F.radians(F.col("start_station_longitude"))
    lat2 = F.radians(F.col("end_station_latitude"))
    lon2 = F.radians(F.col("end_station_longitude"))

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = F.pow(F.sin(dlat / 2.0), 2.0) + F.cos(lat1) * F.cos(lat2) * F.pow(F.sin(dlon / 2.0), 2.0)
    c = 2.0 * F.atan2(F.sqrt(a), F.sqrt(1.0 - a))

    dist_meters = F.lit(EARTH_RADIUS_IN_METERS) * c
    dist_miles = dist_meters / F.lit(METERS_PER_MILE)

    return dataframe.withColumn("distance", F.round(dist_miles, 2).cast(DoubleType()))

def run(spark: SparkSession, input_dataset_path: str, transformed_dataset_path: str) -> None:
    df = spark.read.parquet(input_dataset_path)
    df_out = compute_distance(spark, df).orderBy("starttime")
    df_out.write.parquet(transformed_dataset_path, mode="append")
