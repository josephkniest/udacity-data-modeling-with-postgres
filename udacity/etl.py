import os
import glob
import psycopg2
import json
from sql_queries import *


def process_song_file(cur, filepath):
    # open song file
    df = open(filepath, "r")

    # insert song record
    content = df.read()
    song_data = json.loads(content)
    df.close()

    # insert artist record
    cur.execute(
      artist_table_insert,
      (song_data["artist_id"], song_data["artist_name"], song_data["artist_location"], song_data["artist_latitude"], song_data["artist_longitude"])
    )

    cur.execute(
      song_table_insert, 
      (song_data["song_id"], song_data["artist_id"], song_data["title"], song_data["duration"], song_data["year"])
    )
    


def process_log_file(cur, filepath):
    # open log file
    df = 0

    # filter by NextSong action
    df = 0

    # convert timestamp column to datetime
    t = 0
    
    # insert time data records
    time_data = 0
    column_labels = 0
    time_df = 0

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = 0

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = 0
        cur.execute(songplay_table_insert, songplay_data)


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
    #process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()

