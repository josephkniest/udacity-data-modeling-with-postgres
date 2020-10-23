import psycopg2

def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=postgres password=postgres")
    cur = conn.cursor()

    cur.execute("SELECT * FROM songplays")

    full_song_plays = []
    for rec in cur:
        if rec[1] is not None and rec[5] is not None and rec[8] is not None:
            full_song_plays.append(rec)

    print("Error: Did not find a valid song play" if len(full_song_plays) == 0 else full_song_plays)

    conn.close()

if __name__ == "__main__":
    main()
