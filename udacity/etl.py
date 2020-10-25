import os
import glob
import psycopg2
import json
import datetime
import math
from sql_queries import *


def process_song_file(cur, filepath):

    """process_song_file

    Process a track json file by extracting the song and artist and inserting
    them into their respective postgres tables

    Parameters:
    cur (cursor): Database cursor
    filepath (string): Full path to the file in question

    """

    # open song file
    df = open(filepath, "r")

    # insert song record
    content = df.read()
    song_data = json.loads(content)
    df.close()

    cur.execute(
        artist_table_insert,
        (song_data["artist_id"], song_data["artist_name"], song_data["artist_location"], song_data["artist_latitude"], song_data["artist_longitude"])
    )

    cur.execute(
        song_table_insert,
        (song_data["song_id"], song_data["artist_id"], song_data["title"], song_data["duration"], song_data["year"])
    )


def insert_user(cur, record):

    """insert_user

    Process an event json file by extracting the user and inserting
    them into the user postgres tables

    Parameters:
    cur (cursor): Database cursor
    filepath (dictionary): Parsed json file as a record

    """
    if record["firstName"] is not None and record["lastName"] is not None:
        cur.execute(
            user_table_insert,
            (record["userId"], record["firstName"], record["lastName"], record["gender"], record["level"])
        )


dayOfTheWeek = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

def insert_songplay(cur, record):

    """insert_songplay

    Process an event json file by inserting the event as a songplay
    Attempts to find the song, artist and user id of the songplay

    Parameters:
    cur (cursor): Database cursor
    filepath (dictionary): Parsed json file as a record

    """

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
    song_id = None
    artist_id = None
    user_id = None
    if song is not None:
        song_id = song[0]
        artist_id = song[1]

        # Search for the user by first\last name
        cur.execute("SELECT * FROM users WHERE first_name = %s AND last_name = %s", (record["firstName"], record["lastName"]))
        user = None
        for rec in cur:
            user = rec

        user_id = None if user is None else user[0]

    cur.execute(
      songplay_table_insert,
      (artist_id, record["level"], record["location"], record["sessionId"], song_id, record["ts"], record["userAgent"], user_id)
    )

def process_log_file(cur, filepath):

    """process_log_file

    Process an event json file by extracting and inserting song users, songplays and time

    Parameters:
    cur (cursor): Database cursor
    filepath (string): Full path to the file in question

    """

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
        insert_user(cur, record)
        # insert song plays
        insert_songplay(cur, record)

def process_data(cur, conn, filepath, func):

    """process_data

    Process all event json files and track files and insert the
    data gleaned therein into their respective postgres tables

    Parameters:
    cur (cursor): Database cursor
    conn : Database connection
    filepath (string): Full path to the song or event data sub dir
    func: Process data function

    """

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

