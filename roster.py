import json
import sqlite3

conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()

# Do some setup. Remove existing tables if they are there (allows code to be ran again during iteration) and then generate desired tables. Unique used to make good data entry later on - logical key 
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

#ask for file name, if none then select pre-determined file
fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'roster_data.json'

#Opens and reads the file, creates an array of arrays to work with 
str_data = open(fname).read()
json_data = json.loads(str_data)

for entry in json_data:

    #Establish name and entry for data generation next 
    name = entry[0]
    title = entry[1]
    role = entry[2]

    print((name, title, role))

    #Generate data for tables. IGNORE function built-in to prevent duplication where we don't want it. No need for a 'Limit 1' clause as the unique established earlier would make that redundant 
    cur.execute('''INSERT OR IGNORE INTO User (name)
        VALUES ( ? )''', ( name, ) )
    cur.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    user_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Course (title)
        VALUES ( ? )''', ( title, ) )
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role) VALUES ( ?, ?, ? )''',
        ( user_id, course_id, role) )

    conn.commit()
