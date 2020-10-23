# Sparkify song play aggregation

Sparkify currently stores song play instance data in log form in a series of json files on disc.
This instrumentation loads the song play records as well as the song records themselves (also in
json format on disc to begin with) into a postgres star schema

## Postgres

Both the default database name and postgres root user name are "postgres" instead of "student",
when attempting to compose testing utilities for the etl scripting this will need to be considered.

Connect locally thereto with ```psql postgresql://postgres:postgres@127.0.0.1/sparkifydb```

#### Schema

songplays: This table is the fact table that contains which users listened to what songs at what time
  - songplay_id: The serial ID of the song play instance
  - start_time: This is the milliseconds timestamp when the songplay instance occurred
  - user_id: ID of the user who listened to the song. This might be null.
  - level: Whether or not the user's subscription is "paid" or "free"
  - song_id: ID of the song that was listened to
  - artist_id: ID of the artist who composed the song that was listened to
  - session_id: Appears to be the web session id
  - location: Readable location, city, state
  - user_agent: Device by which the song was listened to, e.g. Firefox on macos

users: The set of known users
  - user_id: ID of the user
  - firstName: User first name
  - lastName: User last name
  - gender: User gender "M"\"F"
  - level: Whether or not the user's subscription is "paid" or "free"

songs: Set of known songs
  - song_id: ID of the song
  - title: Song title
  - artist_id: ID of the artist who composed the song
  - year: Year the song was composed
  - duration: Duration of the song in seconds

artists: Set of known song artists
  - artist_id: ID of the artist
  - name: First and last name of artist
  - location: Readable location, city, state of the artist
  - latitude: Artist's latitude
  - longitude: Artist's longitude

time: Breakdowns of song play instance timestamps
  - start_time: The raw milliseconds play start
  - hour: The hour of the songplay (0 - 23)
  - day: Day of the month of the songplay
  - week: Week of the year of the songplay
  - month: Month of the year of the songplay
  - year: Year of the songplay
  - weekday: Day of the week, e.g. "Monday"

## ETL

The ETL process itself reads files off disc and loads them into the "sparkifydb" database within
the postgres instance. This ETL script set assumes that the data in the logs is non-conflicting,
meaning that although some missing data points may be missing, there will not be two records with
the same user ID mapping to two different values for user's first name.

#### Artists and songs

For song data, the ETL extracts both the artist's information and the song's information and inserts
them as records into postgres. Upon inspection of the data, artists can author many songs but sometimes
they are listed with missing info, so the etl fills in those missing attributes as best it can from
recurrences in the same record

#### Users, song plays and time

Users are extracted from the logs. The etl attempts to fill in as much missing data on the user as
possible when the same user appears more than once. Each log entry is treated as a songplay. A songplay
record is insert regardless of whether or not the etl is able to lookup the song, artist and user id

#### The python files

"create_tables.py" - Resets the postgres sparkify db by dropping all tables and creating new copies

"etl.py" - Walks the filesystem within the "data" directory, loads the json into memory and inserts the
longs into postgres according to the schema

"sql_queries.py" - Contains the sql queries used to create and populate tables

## Constructing postgres database

1) Lay down or replace the schema and data with ```python(|3) create_tables.py```

2) Insert data with ```python(|3) etl.py``` (script set assumes the location of the logs to be in "./data/<etc>")

## Docker image

There's a docker image with the necessary instrumentation baked in (postgres, python 3)

1) Purge any images/containers with ```purge.sh```

2) Generate a new image with ```build.sh```

3) Fire up and get a bash session inside the container with ```run.sh```
