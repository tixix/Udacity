# Sparkify song play logs ETL process
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app
This project extract, transform and loads 5 tables from the Sparkify app logs:
  - `songplays`
 - `users`
 - `songs`
 - `artists`
 - `time` - breaks timestamps into comprehensible columns with time chunks 

## Running the ETL

First create the PostgreSQL database structure:

```
python create_tables.py
```

Then parse the logs files:

```
python etl.py
```

## Database Schema

We have one fact table `songplays` and 4  Dimension table.

### Song Plays table

- *Name:* `songplays`
- *Type:* Fact table

| Column | Type | Description |
| ------ | ---- | ----------- |
| `songplay_id` | `INTEGER` | The main identification of the table | 
| `start_time` | `TIMESTAMP NOT NULL` | The timestamp that this song play log happened |
| `user_id` | `INTEGER NOT NULL` | The user id that triggered this song play log. It cannot be null, as we don't have song play logs without being triggered by an user.  |
| `level` | `VARCHAR` | The level of the user that triggered this song play log |
| `song_id` | `VARCHAR ` | The identification of the song that was played. It can be null.  |
| `artist_id` | `VARCHAR` | The identification of the artist of the song that was played. |
| `session_id` | `INTEGER NOT NULL` | The session_id of the user on the app |
| `location` | `VARCHAR` | The location where this song play log was triggered  |
| `user_agent` | `VARCHAR` | The user agent of our app |

### Users table

- *Name:* `users`
- *Type:* Dimension table

| Column | Type | Description |
| ------ | ---- | ----------- |
| `user_id` | `INTEGER PRIMARY KEY` | The main identification of an user |
| `first_name` | `VARCHAR NOT NULL` | First name of the user, can not be null. It is the basic information we have from the user |
| `last_name` | `VARCHAR NOT NULL` | Last name of the user. |
| `gender` | `VARCHAR` | The gender is stated with just one character `M` (male) or `F` (female). Otherwise it can be stated as `NULL` |
| `level` | `VARCHAR NOT NULL` | The level stands for the user app plans (`premium` or `free`) |


### Songs table

- *Name:* `songs`
- *Type:* Dimension table

| Column | Type | Description |
| ------ | ---- | ----------- |
| `song_id` | `VARCHAR PRIMARY KEY` | The main identification of a song | 
| `title` | `VARCHAR NOT NULL` | The title of the song. It can not be null, as it is the basic information we have about a song. |
| `artist_id` | `VARCHAR NOT NULL REFERENCES artists (artist_id)` | The artist id, it can not be null as we don't have songs without an artist, and this field also references the artists table. |
| `year` | `INTEGER NOT NULL` | The year that this song was made |
| `duration` | `NUMERIC (15, 5) NOT NULL` | The duration of the song |


### Artists table

- *Name:* `artists`
- *Type:* Dimension table

| Column | Type | Description |
| ------ | ---- | ----------- |
| `artist_id` | `VARCHAR PRIMARY KEY` | The main identification of an artist |
| `name` | `VARCHAR NOT NULL` | The name of the artist |
| `location` | `VARCHAR` | The location where the artist are from |
| `latitude` | `NUMERIC` | The latitude of the location that the artist are from |
| `longitude` | `NUMERIC` | The longitude of the location that the artist are from |

### Time table

- *Name:* `time`
- *Type:* Dimension table

| Column | Type | Description |
| ------ | ---- | ----------- |
| `start_time` | `TIMESTAMP  PRIMARY KEY` | The timestamp itself, serves as the main identification of this table |
| `hour` | `NUMERIC NOT NULL` | The hour from the timestamp  |
| `day` | `NUMERIC NOT NULL` | The day of the month from the timestamp |
| `week` | `NUMERIC NOT NULL` | The week of the year from the timestamp |
| `month` | `NUMERIC NOT NULL` | The month of the year from the timestamp |
| `year` | `NUMERIC NOT NULL` | The year from the timestamp |
| `weekday` | `NUMERIC NOT NULL` | The week day from the timestamp |
