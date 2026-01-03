import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, size, explode, countDistinct, sum

# from database.cockroachdb import get_cockroach_connection

# MongoDB connection details
MONGO_ATLAS_URI = "mongodb+srv://shbpndr:CrVz9nzipaLOZFVk@sounds-similar.8sd8tnl.mongodb.net/"
MONGO_DB = "music"
MONGO_COLLECTION_TRACKS = "tracks_metadata"
MONGO_COLLECTION_ARTIST = "artist"
MONGO_COLLECTION_ALBUMS = "albums"
MONGO_COLLECTION_USERS = "users"

os.environ['HADOOP_HOME'] = "C:\\hadoop"
os.environ['hadoop.home.dir'] = "C:\\hadoop"

# Initialize Spark session with MongoDB connector package
spark = SparkSession.builder \
    .appName("Spark MongoDB Operations") \
    .config("spark.mongodb.input.uri", f"{MONGO_ATLAS_URI}{MONGO_DB}.{MONGO_COLLECTION_TRACKS}") \
    .config("spark.mongodb.output.uri", f"{MONGO_ATLAS_URI}{MONGO_DB}.{MONGO_COLLECTION_TRACKS}") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.0") \
    .getOrCreate()

# Load data from the MongoDB collections
tracks_df = spark.read.format("mongodb").option("database", MONGO_DB).option("collection", MONGO_COLLECTION_TRACKS).load()
artists_df = spark.read.format("mongodb").option("database", MONGO_DB).option("collection", MONGO_COLLECTION_ARTIST).load()
albums_df = spark.read.format("mongodb").option("database", MONGO_DB).option("collection", MONGO_COLLECTION_ALBUMS).load()
users_df = spark.read.format("mongodb").option("database", MONGO_DB).option("collection", MONGO_COLLECTION_USERS).load()

# Show the schema of each DataFrame to check the structure of the data
print("Schema of the tracks collection:")
tracks_df.printSchema()

print("Schema of the artists collection:")
artists_df.printSchema()

print("Schema of the albums collection:")
albums_df.printSchema()

print("Schema of the users collection:")
users_df.printSchema()

# Example Queries

# 1. Show the first 5 artists (general query)
print("First 5 artists:")
artists_df.show(5)

# 2. Count the total number of albums in the database (general query)
print("Total number of albums:")
total_albums_count_df = albums_df.count()
print(f"Total number of albums: {total_albums_count_df}")

# 3. Show all albums released after a specific playcount threshold (general query)
print("Albums with playcount greater than 5 million:")
albums_above_5_million_df = albums_df.filter(col("playcount").cast("int") > 5000000)
albums_above_5_million_df.show()

# 4. List the artists that have no tags (general query)
print("Artists with no tags:")
artists_no_tags_df = artists_df.filter(size(col("tags")) == 0)
artists_no_tags_df.show()

# 5. Count the number of albums by each artist (general query)
print("Number of albums by each artist:")
album_count_by_artist_df = albums_df.groupBy("artist").count().orderBy("count", ascending=False)
album_count_by_artist_df.show()

# 6. Find the albums with the highest number of listeners (general query)
print("Top 5 albums with the highest number of listeners:")
top_5_albums_by_listeners_df = albums_df.orderBy(col("listeners").desc()).limit(5)
top_5_albums_by_listeners_df.show()

# 7. Find the total number of tracks in the database (general query)
print("Total number of tracks in the database:")
total_tracks_count_df = tracks_df.count()
print(f"Total number of tracks: {total_tracks_count_df}")

# 8. Show the album with the highest playcount (general query)
print("Album with the highest playcount:")
highest_playcount_album_df = albums_df.orderBy(col("playcount").desc()).limit(1)
highest_playcount_album_df.show()

# 9. List all tracks in the database, showing their artist and album (general query)
print("All tracks with their artist and album:")
all_tracks_df = tracks_df.select("track", "artist", "album")
all_tracks_df.show()

# 10. Find the average playcount of all albums (general query)
print("Average playcount of all albums:")
avg_playcount_df = albums_df.agg({"playcount": "avg"}).show()

# 11. Find all tracks with more than 5 artists associated with them (general query)
print("Tracks with more than 5 artists:")
tracks_with_more_than_5_artists_df = tracks_df.filter(size(col("artist")) > 5)
tracks_with_more_than_5_artists_df.show()

# 12. Show the artist with the most similar artists (general query)
print("Artist with the most similar artists:")
artist_with_most_similar_artists_df = artists_df.withColumn("similar_count", size(col("similar_artists"))) \
    .orderBy(col("similar_count").desc()).limit(1)
artist_with_most_similar_artists_df.show()

# 13. List albums that have more than 10 tracks (general query)
print("Albums with more than 10 tracks:")
albums_with_more_than_10_tracks_df = albums_df.withColumn("tracks_count", size(col("tracks"))).filter(col("tracks_count") > 10)
albums_with_more_than_10_tracks_df.show()

# 14. List all albums where the tracks array is empty (general query)
print("Albums with no tracks (empty tracks array):")
albums_with_no_tracks_df = albums_df.filter(size(col("tracks")) == 0)
albums_with_no_tracks_df.show()

# 15. Count how many albums have been tagged as 'rock' in their tags (general query)
print("Albums tagged as 'rock':")
rock_tagged_albums_df = albums_df.filter(explode(col("tags")) == "rock").count()
print(f"Total albums tagged as 'rock': {rock_tagged_albums_df}")

# 16. Show all tracks from a specific album (e.g., 'Please Please Me') (general query)
print("Tracks from the album 'Please Please Me':")
please_please_me_tracks_df = tracks_df.filter(col("album") == "Please Please Me")
please_please_me_tracks_df.show()

# 17. Count the distinct number of artists in the database (general query)
print("Distinct number of artists:")
distinct_artists_count_df = artists_df.select("name").distinct().count()
print(f"Distinct number of artists: {distinct_artists_count_df}")

# 18. Show all tracks from a specific artist (e.g., 'The Beatles') (general query)
print("Tracks from 'The Beatles':")
beatles_tracks_df = tracks_df.filter(col("artist") == "The Beatles")
beatles_tracks_df.show()

# 19. Show albums sorted by release date (general query)
print("Albums sorted by release date:")
albums_sorted_by_date_df = albums_df.orderBy(col("release_date").desc())
albums_sorted_by_date_df.show()

# Stop the Spark session
spark.stop()
print("Spark session stopped.")
