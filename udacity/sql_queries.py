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
    FOREIGN KEY (artist_id) REFERENCES artists (artist_id),
    auth VARCHAR ( 16 ),
    itemInSession INT NOT NULL,
    length FLOAT ( 24 ),
    level VARCHAR ( 64 ),
    location VARCHAR ( 64 ),
    method VARCHAR ( 8 ),
    page VARCHAR ( 16 ),
    registration FLOAT ( 24 ),
    session_id INT NOT NULL,
    song_id VARCHAR ( 96 ),
    FOREIGN KEY (song_id) REFERENCES songs (song_id),
    status INT NOT NULL,
    start_time BIGINT,
    user_agent VARCHAR ( 512 ),
    user_id VARCHAR ( 96 ),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
  )
""")

user_table_create = ("""
  CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR ( 96 ) PRIMARY KEY,
    first_name VARCHAR ( 32 ),
    last_name VARCHAR ( 32 ),
    gender VARCHAR ( 1 ) NOT NULL,
    level VARCHAR ( 64 )
  )
""")

song_table_create = ("""
  CREATE TABLE IF NOT EXISTS songs (
    song_id VARCHAR ( 96 ) PRIMARY KEY,
    artist_id VARCHAR ( 96 ),
    FOREIGN KEY (artist_id) REFERENCES artists (artist_id),
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
    start_time BIGINT,
    hour INT,
    day INT,
    week INT,
    month INT,
    year INT,
    weekday INT
  )
""")

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")


time_table_insert = ("""
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [time_table_create, user_table_create, artist_table_create, song_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

