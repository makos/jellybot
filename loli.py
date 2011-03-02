#!/usr/bin/env python2

import sqlite3
import random
import time

global db, cur

def open():

    global db, cur

    #Open database
    db = sqlite3.connect('lolis.db')

    #Create cursors
    cur = db.cursor()

def save():
    #Commit changes
    db.commit()

    #Close everything
    cur.close()
    db.close()

def create ():
    """Creates table structure"""

    #if table not found - create table
    cur.execute( 'CREATE TABLE IF NOT EXISTS lolis (user TEXT, lolis INTEGER, time INTEGER)' )
    #except sqlite3.OperationalError, msg:
    #print msg

def add( user, lolis ):
    """Insert new user in database"""

    #Gets current time
    thetime = time.time()

    #Insert user data into table
    cur.execute( 'INSERT INTO lolis VALUES ("{}", "{}", "{}")'.format( user, lolis, int(thetime) ) )

def update( user, lolis ):
    """Updates user data"""

    #Gets current time
    thetime = time.time()

    #Find user and update loli count and timestamp
    cur.execute( 'UPDATE lolis SET lolis = "{}", time = "{}" WHERE user = "{}"'.format( lolis, int(thetime), user ) )

def load( user ):
    """Loads user data"""

    cur.execute('SELECT lolis, time FROM lolis WHERE user="{}"'.format(user))

    #Fetch all data from our querie
    data = cur.fetchall()

    return data

def loli( user, time):

    #Interval between command in seconds
    #6 hours should be sane interval
    interval = 3600 #Keeping it at 5 seconds for testing purposes

    #Min and Max # of lolis you can get
    min_lolis = 0
    max_lolis = 15

    #Save mode:
    #   0: Adds new row for user
    #   1: Updates previous record
    mode = 0

    #Loads user data
    data = load( user )

    #Set default starting values
    lolis = 0
    last_usage = 0

    #If we did load anything, assign values
    if( data ):
        lolis = data[0][0]
        last_usage = data[0][1]

    #If timestamp is greater than zero, set mode to update data
    if ( last_usage > 0 ):
        mode = 1

    #Little debug message
    #print "--> Time: {} Save time: {} Difference: {}".format(time, last_usage, time - last_usage)

    #Check cooldown interval
    if( (int(time) - int(last_usage)) < interval ):
        output = "Calm down, {}".format( user )
        return output

    #Generate random number from min to max value
    newlolis = random.randint( min_lolis, max_lolis)

    #Add new value to total number of lolis
    lolis += newlolis

    #Announce results
    if newlolis == 0:
        output = "Fukou da. {} didn't get any lolis this time, but {} still has {} lolis left.".format( user, user, lolis )
    elif newlolis == 1:
        output = "{} got one more loli, {} now has {} lolis in total!".format( user, user, lolis)
    elif newlolis > 10:
        output = "{} is SUPER PEDO and got {} lolis and {} already has {}".format( user, newlolis, user, lolis )
    elif newlolis > 5:
        output = "{} was lucky this time, he escaped paryvan with {} lolis and bitches still don't know 'bout his {} lolis.". format( user, newlolis, lolis )
    else:
        output = "{} got, {} lolis! And has total of {} lolis!".format( user, newlolis, lolis)

    print output;
    #Save data
    if mode == 0:
        #Insert new user
        add( user, lolis )
    elif mode == 1:
        #Update previous record
        update( user, lolis)

    return output

if __name__ == "__main__":

    open()

    #Try to create table in database
    create()

    loli("fatapaca", time.time())
    loli("makos", time.time())

    save()
