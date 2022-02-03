### Data preparation

#### Start a local Redis docker container
```
docker run --name my-redis -p 6379:6379 -d redis
```
  
#### Download and prepare movielens (1 million records) dataset for Machine Learning:
```
curl -O 'http://files.grouplens.org/datasets/movielens/ml-1m.zip'
unzip ml-1m.zip
sed 's/::/,/g' ml-1m/ratings.dat > ratings.csv
sed 's/::/@/g' ml-1m/movies.dat > movie_titles.csv
sed 's/::/,/g' ml-1m/users.dat > users.csv
```

Load movies: 
``` 
cat movie_titles.csv | awk -F \
"@" '{printf "hset movie_title:%s movie_title \"%s\" genre \"%s\"\n",$1,$2,$3;}' \
| redis-cli -p 6379
```
Inside Redis as Hash:  
Key: movie_titles:{movie_id}
Fields: movie_title, genre

Load ratings:  
```
cat ratings.csv | awk -F "," \
'{printf "hset movie_rating:%s:%s rating \"%s\" timestamp \"%s\"\n",$1,$2,$3,$4;}' \
| redis-cli -p 6379
```

Inside Redis as Hash:
Key: movie_rating:{user_id}:{movie_id}
Fields: rating, timestamp
    
Load movie ids:
```
cat movie_titles.csv | awk -F "@" '{printf "sadd movies %s\n",$1;}' | redis-cli -p 6379
```
  
Load user ids:
```
cat users.csv | awk -F "," '{printf "sadd users %s\n",$1;}' | redis-cli -p 6379
```
    
Load user_ratings:
```
cat ratings.csv | awk -F "," '{printf "sadd user_ratings %s:%s\n",$1,$2;}' | redis-cli -p 6379
```
  

