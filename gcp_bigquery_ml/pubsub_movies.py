from google.cloud import pubsub_v1
import json
import redis


# Initialization
project_id = "central-beach-194106"
publisher = pubsub_v1.PublisherClient()
redis = redis.StrictRedis(host='127.0.0.1', port='6379', password=None, decode_responses=True)


# Publish movie ratings data to GCP PubSub
topic_id = "glau-movielens_1m"
topic_path = publisher.topic_path(project_id, topic_id)
user_ratings = redis.smembers("user_ratings")
for m in user_ratings:
  user_movie = m.split(':')
  value = redis.hgetall("movie_rating:" + user_movie[0] + ":" + user_movie[1])
  data = {"user_id": user_movie[0],
          "item_id": user_movie[1],
          "rating": value["rating"],
          "timestamp": value["timestamp"] }
  data_str = json.dumps(data)
  # Data must be a bytestring
  data = data_str.encode("utf-8")
  future = publisher.publish(topic_path, data)
  print(future.result())


# Publish movie titles data to GCP PubSub
topic_id = "glau-movie_titles"
topic_path = publisher.topic_path(project_id, topic_id)
movies = redis.smembers("movies")
for m in movies:
  value = redis.hgetall("movie_title:" + m)
  data = {"movie_id": m,
          "movie_title": value["movie_title"],
          "genre": value["genre"] }
  data_str = json.dumps(data)
  # Data must be a bytestring
  data = data_str.encode("utf-8")
  future = publisher.publish(topic_path, data)
  print(future.result())

