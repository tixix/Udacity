import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Process songs log file
    :param cur: the cursor object
    :param filepath: log data file path
    :return: None
    """
    # open song file
    df = pd.read_json(filepath,  lines=True)

    # insert song record
    columns = [ 'song_id', 'title', 'artist_id', 'year', 'duration']
    song_data = df[columns].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    cols = ['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']
    artist_data = df[cols].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Process a songsplay log file
    :param cur: The cursor object
    :param filepath: The path to the log file
    :return:None
    """
    # open log file
    df = pd.read_json(filepath, lines=True)  

    # filter by NextSong action
    df = df[df['page'] == 'NextSong'] 

    # convert timestamp column to datetime
    t =  pd.to_datetime(df['ts'], unit='ms') 

    # insert time data records
    hour  = t.dt.hour
    day = t.dt.day
    week_of_year = t.dt.weekofyear
    month = t.dt.month
    year = t.dt.year
    weekday = t.dt.weekday
    
    time_data = [t, hour, day, week_of_year, month, year, weekday]
    column_labels = ['start_time', 'hour', 'day', 'week_of_year', 'month', 'year' , 'weekday']
    time_df = pd.DataFrame(dict(zip(column_labels, time_data))) 

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    cols_user = ['userId','firstName', 'lastName', 'gender', 'level' ]
    user_df = df[cols_user]

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
        songplay_data = (index, pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)
#         conn.commit()


def process_data(cur, conn, filepath, func):
    """
    Process all the data executing the given func for every *.json file of the given filepath
    :param cur: The cursor data
    :param conn: The connection with postgresql
    :param filepath: The logs folder path
    :param func: The function to process one log file per time
    :return:None
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
    """
    The main function
    :return: None
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()