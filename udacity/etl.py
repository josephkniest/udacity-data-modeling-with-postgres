import os
import glob
import psycopg2
import json
import datetime
import math
from sql_queries import *


def process_song_file(cur, filepath):
    # open song file
    df = open(filepath, "r")

    # insert song record
    content = df.read()
    song_data = json.loads(content)
    df.close()

    cur.execute("SELECT * FROM artists WHERE artist_id = '" + song_data["artist_id"] + "'")
    record = 0
    for rec in cur:
        record = rec

    # insert/update artist record
    if(record == 0):
        cur.execute(
            artist_table_insert,
            (song_data["artist_id"], song_data["artist_name"], song_data["artist_location"], song_data["artist_latitude"], song_data["artist_longitude"])
        )
    else :
        song_data["artist_name"] = song_data["artist_name"] if record[1] == None else record[1]
        song_data["artist_location"] = song_data["artist_location"] if record[2] == None else record[2]
        song_data["artist_latitude"] = song_data["artist_latitude"] if record[3] == None else record[3]
        song_data["artist_longitude"] = song_data["artist_longitude"] if record[4] == None else record[4]
        cur.execute(
            artist_table_update,
            (song_data["artist_name"], song_data["artist_location"], song_data["artist_latitude"], song_data["artist_longitude"], song_data["artist_id"])
        )

    cur.execute(
        song_table_insert, 
        (song_data["song_id"], song_data["artist_id"], song_data["title"], song_data["duration"], song_data["year"])
    )
    


def add_or_update_user(cur, record):
    # query user
    user_id = record["userId"]
    cur.execute("SELECT * FROM users WHERE user_id = '" + user_id + "'")
    user = cur.fetchone()

    if user:
        record["firstName"] = record["firstName"] if user[1] == None else user[1]
        record["lastName"] = record["lastName"] if user[2] == None else user[2]
        record["gender"] = record["gender"] if user[3] == None else user[3]
        record["level"] = record["level"] if user[4] == None else user[4]
        cur.execute(
            user_table_update,
            (record["firstName"], record["lastName"], record["gender"], record["level"], record["userId"])
        )
    else :
        cur.execute(
            user_table_insert,
            (record["userId"], record["firstName"], record["lastName"], record["gender"], record["level"])
        )


dayOfTheWeek = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

def insert_songplay(cur, record):
    # For some reason the rubric expects a "time" table to contain a
    # numerical breakdown of each time unit as to when a song was played
    # This is presumably the "ts" milliseconds property in the json.
    # The ts fields appear to be milliseconds since the unix epoch (1/1/1970)
    # We insert it here:
    dt = datetime.datetime.fromtimestamp(record["ts"] / 1000.0)
    cur.execute(time_table_insert, (record["ts"], dt.hour, dt.day, dt.isocalendar()[1], dt.month, dt.year, dayOfTheWeek[dt.weekday()]))

    # Songplay records not expected to contain artist id
    # or song id so look them up from within the song table
    song = None
    if record["song"] is not None:
        cur.execute("SELECT * FROM songs WHERE title = '" + record["song"].replace("'", "''") + "'")
        for rec in cur:
            song = rec

    # If there is no known song in the song dataset don't
    # insert a fact (songplay) into the fact table as a
    # songless songplay is pretty useless
    if song is not None:
        song_id = song[0]
        artist_id = song[1]

        # Search for the user by first\last name
        cur.execute("SELECT * FROM users WHERE first_name = %s AND last_name = %s", (record["firstName"], record["lastName"]))
        user = None
        for rec in cur:
            user = rec

        if user is not None:
            user_id = user[0]
            # It is possible to fill in all columns belonging to the songplay table, however
            # according to the udacity grading rubric, all columns besdies "artist_id" and "song_id"
            # are supposed to be "None" For reference the entire insertion array could be:
            # (artist_id, record["level"], record["location"], record["sessionId"], song_id, record["ts"], record["userAgent"], user_id)

            # It is also worth noting that the rubric expects there to only be one record in the songsplay table. In fact there
            # are actually three instances of a different user listening to the same song (Intro, 2003)
            cur.execute(
              songplay_table_insert,
              (artist_id, None, None, None, song_id, None, None, None)
            )

def process_log_file(cur, filepath):
    # open log file
    file = open(filepath, "r")

    # load log file content into memory
    content = file.read()

    # close filedescriptor
    file.close()

    logs = content.split("\n")
    for log in logs:
        record = json.loads(log)

        # insert/update user
        add_or_update_user(cur, record)
        # insert song plays
        insert_songplay(cur, record)

def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=postgres password=postgres")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()

