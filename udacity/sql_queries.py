# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users "
song_table_drop = "DROP TABLE  IF EXISTS songs"
artist_table_drop = "DROP TABLE  IF EXISTS artists"
time_table_drop = "DROP TABLE  IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
  CREATE TABLE IF NOT EXISTS songplays (
    songplay_id SERIAL PRIMARY KEY,
    artist_id VARCHAR ( 96 ),
    FOREIGN KEY(artist_id) REFERENCES artists(artist_id),
    level VARCHAR ( 64 ),
    location VARCHAR ( 64 ),
    session_id INT,
    song_id VARCHAR ( 96 ),
    FOREIGN KEY(song_id) REFERENCES songs(song_id),
    start_time BIGINT,
    user_agent VARCHAR ( 512 ),
    user_id VARCHAR ( 96 ),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
  )
""")

user_table_create = ("""
  CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR ( 96 ) PRIMARY KEY,
    first_name VARCHAR ( 32 ) NOT NULL,
    last_name VARCHAR ( 32 ) NOT NULL,
    gender VARCHAR ( 1 ),
    level VARCHAR ( 64 )
  )
""")

song_table_create = ("""
  CREATE TABLE IF NOT EXISTS songs (
    song_id VARCHAR ( 96 ) PRIMARY KEY,
    artist_id VARCHAR ( 96 ),
    title VARCHAR ( 128 ),
    duration FLOAT ( 24 ),
    year INT
  )
""")

artist_table_create = ("""
  CREATE TABLE IF NOT EXISTS artists (
    artist_id VARCHAR ( 96 ) PRIMARY KEY,
    name VARCHAR ( 96 ),
    location VARCHAR ( 96 ),
    latitude FLOAT ( 24 ),
    longitude FLOAT ( 24 )
  )
""")

time_table_create = ("""
  CREATE TABLE IF NOT EXISTS time (
    time_id SERIAL PRIMARY KEY,
    start_time BIGINT NOT NULL,
    hour INT NOT NULL,
    day INT NOT NULL,
    week INT NOT NULL,
    month INT NOT NULL,
    year INT NOT NULL,
    weekday VARCHAR ( 10 ) NOT NULL
  )
""")

# INSERT RECORDS

songplay_table_insert = ("""
  INSERT INTO songplays (artist_id, level, location, session_id, song_id, start_time, user_agent, user_id)
  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
  INSERT INTO users (user_id, first_name, last_name, gender, level) 
  VALUES (%s, %s, %s, %s, %s)
  ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level
""")

user_table_update = ("""
  UPDATE users SET
    first_name = %s,
    last_name = %s,
    gender = %s,
    level = %s
  WHERE user_id = %s
""")

song_table_insert = ("""
  INSERT INTO songs (song_id, artist_id, title, duration, year) 
  VALUES (%s, %s, %s, %s, %s)
""")

artist_table_insert = ("""
  INSERT INTO artists (artist_id, name, location, latitude, longitude) 
  VALUES (%s, %s, %s, %s, %s)
""")

artist_table_update = ("""
  UPDATE artists SET 
    name = %s,
    location = %s,
    latitude = %s,
    longitude = %s
  WHERE artist_id = %s 
""")

time_table_insert = ("""
  INSERT INTO time (start_time, hour, day, week, month, year, weekday)
  VALUES (%s, %s, %s, %s, %s, %s, %s)
""")

# QUERY LISTS

create_table_queries = [time_table_create, user_table_create, artist_table_create, song_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]


