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
    data = cur.fetchone()

    return data

def loli( user ):

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
        lolis = data[0]
        last_usage = data[1]

    #If timestamp is greater than zero, set mode to update data
    if ( last_usage > 0 ):
        mode = 1

    #Check cooldown interval
    if( (int(time.time()) - int(last_usage)) < interval ):
        return

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
        output = "{} was lucky this time, he escaped partyvan with {} lolis and bitches still don't know 'bout his {} lolis.". format( user, newlolis, lolis )
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

def steal( caller, target ):

    if caller == target:
        return

    #Min and Max # of lolis you can get
    min_lolis = 0
    max_lolis = 10

    #Save mode
    c_mode = 0
    t_mode = 0

    #Loads user data
    _caller = load( caller )
    _target = load( target )

    #Target has no lolis
    if not _target:
        return

    #Interval between command in seconds
    interval = 3600
    thetime   = int(time.time())
    timestamp = int(_caller[1])

    #Check interval
    if( ( thetime - timestamp ) < interval ):
        return

    #Generate random number from min to max value
    loot = random.randint( min_lolis, max_lolis)

    #If timestamp is greater than zero, set mode to update data
    if ( _caller[1] > 0 ):
        c_mode = 1

    if ( _target[1] > 0 ):
        t_mode = 1

    # Don't let caller's loot exceed target's lolis
    if ( loot > _target[0] ):
        loot = _target[0]

    # Add new lolis to callers stash
    c_lolis = ( _caller[0] + loot )

    # Remove lolis from target
    t_lolis = ( _target[0] - loot )

    #Save callers data
    if c_mode == 0:
        add( caller, c_lolis )
    elif c_mode == 1:
        update( caller, c_lolis)

    if loot <= 0:
        return "{} couldn't steal any lolis from {}".format( caller, target )

    #Save targets data
    if t_mode == 0:
        #shouldn't happen
        add( target, t_lolis )
    elif t_mode == 1:
        update( target, t_lolis)

    return "{} stole {} lolis from {} and now has a total of {} lolis.".format( caller, loot, target, c_lolis )

if __name__ == "__main__":

    open()

    #Try to create table in database
    create()

    loli("fatapaca", time.time())
    loli("makos", time.time())

    save()
