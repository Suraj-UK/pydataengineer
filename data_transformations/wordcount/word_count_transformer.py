import logging
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F


def tokenise(df: DataFrame) -> DataFrame:
    """
    Lowercase, keep letters and apostrophes, split on whitespace,
    drop empty tokens or tokens made only of apostrophes.
    """
    cleaned = F.regexp_replace(F.lower(F.col("value")), r"[^a-z']+", " ")
    tokens = F.split(F.trim(cleaned), r"\s+")
    words = (
        df.select(tokens.alias("tokens"))
          .select(F.explode("tokens").alias("word"))
          .filter(F.col("word") != "")
          .filter(~F.col("word").rlike(r"^'+$"))
    )
    return words


def run(spark: SparkSession, input_path: str, output_path: str) -> None:

    input_df = spark.read.text(input_path)
    words_df = tokenise(input_df)
    counts_df = (
        words_df.groupBy("word").count()
        .select("word", F.col("count").alias("count"))
        .orderBy("word")
    )

    logging.info("Writing csv to directory: %s", output_path)
    counts_df.coalesce(1).write.mode("overwrite").option("header", True).csv(output_path)
