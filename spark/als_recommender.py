from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.functions import rand

spark = SparkSession.builder \
    .appName("MovieLens ALS Recommender") \
    .master("local[*]") \
    .getOrCreate()

base_path = "hdfs://localhost:9000/user/shrika/movielens/ml-latest-small"

ratings = spark.read.csv(
    f"{base_path}/ratings.csv",
    header=True,
    inferSchema=True
).select("userId", "movieId", "rating")

movies = spark.read.csv(
    f"{base_path}/movies.csv",
    header=True,
    inferSchema=True
).select("movieId", "title")

als = ALS(
    userCol="userId",
    itemCol="movieId",
    ratingCol="rating",
    rank=10,
    maxIter=10,
    regParam=0.1,
    nonnegative=True,
    coldStartStrategy="drop"
)

model = als.fit(ratings)

# Recommend movies for a sample user
user_id = ratings \
    .select("userId") \
    .distinct() \
    .orderBy(rand()) \
    .limit(1) \
    .collect()[0]["userId"]
user_df = spark.createDataFrame([(user_id,)], ["userId"])

recommendations = model.recommendForUserSubset(user_df, 10)

recommendations \
    .selectExpr("explode(recommendations) as rec") \
    .select("rec.movieId", "rec.rating") \
    .join(movies, "movieId") \
    .orderBy("rating", ascending=False) \
    .show(truncate=False)
print(f"These are top 10 recommended movies for user no. {user_id}")

# Analytics - RMSE & MAE

#RMSE (Root Mean Squared Error) - Difference of predicted ratings from actual ratings.
predictions = model.transform(ratings)

evaluator = RegressionEvaluator(
    metricName="rmse",
    labelCol="rating",
    predictionCol="prediction"
)

rmse = evaluator.evaluate(predictions)
print(f"┌───┐\n│RMSE = {rmse}│\n└───┘")

#MAE (Mean Absolute Error) - Average absolute difference between predicted and real ratings.
evaluator = RegressionEvaluator(
    metricName="mae",
    labelCol="rating",
    predictionCol="prediction"
)
mae = evaluator.evaluate(predictions)
print(f"┌───┐\n│MAE = {mae}│\n└───┘")

spark.stop()
