#!/usr/bin/env python2

import sqlite3
import random
import time

global db, cur

def create ():
    """Creates table structure"""

    #if table not found - create table
    cur.execute( 'CREATE TABLE lolis (user TEXT, lolis INTEGER, time INTEGER)' )

    # TODO: Handle db exceptions (eg. table already exists)

    print "Created table"

def add( user, lolis ):
    """Insert new user in database"""

    #Gets current time
    thetime = time.time()

    #Insert user data into table
    cur.execute( 'INSERT INTO lolis VALUES (?, ?, ?)', ( user, lolis, int(thetime) ) )

    print "Added"

def update( user, lolis ):
    """Updates user data"""

    #Gets current time
    thetime = time.time()

    #Find user and update loli count and timestamp
    cur.execute( 'UPDATE lolis SET lolis = ?, time = ? WHERE user = ?', (lolis, int(thetime), user  ))

    print "Updated"

def load( user, what ):

    print "DB: Getting", what, "for user", user
    cur.execute('SELECT "{0}" FROM lolis WHERE user="{1}"'.format(what, user))

    #print cur.fetchall()
    print "DB: Returned", cur.fetchone()
    return cur.fetchone()

def loli( user, time):

    last_usage = time
    interval = 3600

    min_lolis = 0
    max_lolis = 10

    mode = 0

    #Load data?
    lolis = load( user, "lolis" )
    print "Lolis:", lolis
    last_usage = load( user, "time" )
    print "Timestamp:", last_usage

    #if (lolis == 0 or last_usage == 0):
    #    mode = 1

    #if( (int(time) - int(last_usage)) > interval ):
    #    print "Calm down, bro"
    #    return

    lolis = random.randint( min_lolis, max_lolis)

    print user, "got", lolis, "lolis!"

    if mode == 0:
        update( user, lolis)
    elif mode == 1:
        add( user, lolis )

if __name__ == "__main__":

    global db, cur

    print "Opening database"
    db = sqlite3.connect('lolis.db')
    cur = db.cursor()
    print "-> Done"

    #create()

    loli("fatapaca", time.time())
    #loli("makos", time.time())

    db.commit()
    db.close()
    print "Saved and closed"
