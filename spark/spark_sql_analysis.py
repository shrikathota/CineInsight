from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count

spark = SparkSession.builder \
    .appName("MovieLens Spark SQL Analysis") \
    .master("local[*]") \
    .getOrCreate()

base_path = "hdfs://localhost:9000/user/shrika/movielens/ml-latest-small"

# Load CSV files
ratings = spark.read.csv(
    f"{base_path}/ratings.csv",
    header=True,
    inferSchema=True
)

movies = spark.read.csv(
    f"{base_path}/movies.csv",
    header=True,
    inferSchema=True
)

# Register temp views
ratings.createOrReplaceTempView("ratings")
movies.createOrReplaceTempView("movies")

# Top 10 Most Rated Movies
spark.sql("""
    SELECT m.title, COUNT(r.rating) AS rating_count
    FROM ratings r
    JOIN movies m ON r.movieId = m.movieId
    GROUP BY m.title
    ORDER BY rating_count DESC
    LIMIT 10
""").show(truncate=False)
print("\nThese are the Top 10 Most Rated Movies \n")

# Top 10 Highest Rated Movies (min 50 ratings)
spark.sql("""
    SELECT m.title,
           ROUND(AVG(r.rating), 2) AS avg_rating,
           COUNT(*) AS cnt
    FROM ratings r
    JOIN movies m ON r.movieId = m.movieId
    GROUP BY m.title
    HAVING cnt >= 50
    ORDER BY avg_rating DESC
    LIMIT 10
""").show(truncate=False)
print("\nThese are the Top 10 Highest Rated Movies (min 50 ratings) \n")

# Genre-wise Average Rating

from pyspark.sql.functions import explode, split

movies_genres = movies \
    .withColumn("genre", explode(split("genres", "\\|")))

movies_genres.createOrReplaceTempView("movies_genres")

spark.sql("""
SELECT genre, ROUND(AVG(r.rating),2) AS avg_rating
FROM ratings r
JOIN movies_genres m
ON r.movieId = m.movieId
GROUP BY genre
ORDER BY avg_rating DESC
""").show()
print("\nThese are the Genre-wise Average Rating of Movies \n")

spark.stop()
