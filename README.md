# 🎬 CineInsight - A Movie Recommendation & Analysis Engine using Apache Spark

## 📌 Problem Statement

With the rapid growth of online streaming platforms, users are overwhelmed by the sheer number of movies available. Recommender systems help users discover relevant content by analyzing past interactions and preferences.

The goal of this project is to:

- Analyze large-scale movie rating data using **Spark SQL**
- Build a personalized movie recommendation system using **ALS (Alternating Least Squares)**
- Store and process data using a distributed **HDFS** environment
- Demonstrate Big Data concepts such as **distributed storage**, **parallel computation**, and **ML pipelines**

---

## 🛠 Technologies Used

| Category            | Technology                     |
|---------------------|--------------------------------|
| Big Data Framework  | Apache Spark 3.5.1             |
| Storage             | HDFS (Hadoop 3.3.6)            |
| Language            | Python (PySpark)               |
| ML Library          | Spark MLlib (ALS)              |
| Query Engine        | Spark SQL                      |
| Dataset             | MovieLens (ml-latest-small)    |
| OS                  | Ubuntu (WSL2)                  |
| IDE                 | IntelliJ IDEA / VS Code        |

---

## 🧱 Project Architecture
<img width="700" height="650" alt="image" src="https://github.com/user-attachments/assets/902ef41a-ae5a-4060-8b49-1ea2adfaa250" />

## ⚙️ Setup and Installation

### 1️⃣ Prerequisites

Ensure the following are installed:

- Java 11
- Hadoop 3.3.6
- Spark 3.5.1 (Hadoop-compatible build)
- Python 3.12
- WSL2 (Ubuntu)

---

### 2️⃣ Set up your Environment Variables

Add the following to your `.bashrc` or `.zshrc`:

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export HADOOP_HOME=~/hadoop-3.3.6
export SPARK_HOME=~/spark-3.5.1-bin-hadoop3
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$SPARK_HOME/bin
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.7-src.zip
export PYSPARK_PYTHON=python3.11
export PYSPARK_DRIVER_PYTHON=python3.11
```
Add these environment variables using the command :
```bash
nano ~/.bashrc
```
After adding it, save it using the command :
```bash
Ctrl + O  -> Enter
Ctrl + X
```
Now, apply the changes made using the command : 
```bash
source ~/.bashrc
```
## ▶️ How to Run the Application
### Step 1: Start HDFS
```bash
cd ~/hadoop-3.3.6
sbin/start-dfs.sh
jps
```
Ensure 
```bash 
NameNode, DataNode
```
, and 
```bash
SecondaryNameNode
```
are running.

### Step 2: Move Dataset to HDFS
```bash
hdfs dfs -mkdir -p /user/<username>/movielens/ml-latest-small
hdfs dfs -put *.csv /user/<username>/movielens/ml-latest-small
```
Verify:
```bash
hdfs dfs -ls /user/<username>/movielens/ml-latest-small
```
### Step 3: Run Spark SQL Analysis
```bash
cd ~/IdeaProjects/MovieRecommendationSystem
spark-submit spark/spark_sql_analysis.py
```
#### Sample Output (Screenshots) :

##### Top 10 Most Rated Movies
<img width="411" height="446" alt="image" src="https://github.com/user-attachments/assets/8582a56f-7aa7-402f-90d1-bb49b62b13e2" />

##### Top 10 Highest Rated Movies (min 50 ratings)
<img width="411" height="239" alt="Screenshot 2026-02-08 122110" src="https://github.com/user-attachments/assets/e101ec4a-6587-469a-887a-63bfd5d6def7" />

##### Genre-wise Average Rating
<img width="411" height="361" alt="genre" src="https://github.com/user-attachments/assets/58615ad9-1771-4c9a-844d-8caffbecf35c" />

### Step 4: Run ALS Recommendation Engine
```bash
spark-submit spark/als_recommender.py
```
#### Sample Output (Screenshots) :

##### Top 10 movie recommendations for a randomly selected user
<img width="959" height="209" alt="Screenshot 2026-02-08 131050" src="https://github.com/user-attachments/assets/71f6ecf3-94c4-482b-bfc3-a0e4a0822d95" />

##### Evaluation Metrics (RMSE & MAE)
<img width="959" height="41" alt="rmse" src="https://github.com/user-attachments/assets/a93be17a-956b-4e68-92c3-bb5af9d42bd1" />
<img width="959" height="40" alt="mae" src="https://github.com/user-attachments/assets/b5a800a7-5f81-4cfe-8214-a22d52f80419" />

## 📊 Inference

- The ALS model successfully learns latent user and movie factors
- Popular movies tend to have higher rating counts but not always higher ratings
- RMSE and MAE values indicate acceptable prediction accuracy for a dataset containing 100,000 ratings and 3,600 tag applications applied to 9,000 movies by 600 users.
- Using HDFS enables scalable storage and fault tolerance
- Spark SQL efficiently handles analytical queries over large datasets.

## 🚀 Future Work

- Scale to MovieLens 20M / 25M dataset
- Add implicit feedback (views, clicks)
- Implement Top-N ranking metrics (Precision@K, Recall@K)
- Add genre-based recommendations.
- Integrate real-time streaming (Kafka + Spark Streaming)
- Build a REST API / Web UI for recommendations.
- Compare ALS with content-based filtering

Author: Shrika Thota


