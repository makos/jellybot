#!/usr/bin/env python2
import sqlite3
import random
import time

global db, cur

last_top = 0

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
  cur.execute( 'CREATE TABLE IF NOT EXISTS lolis (user TEXT, lolis INTEGER, time INTEGER, stime INTEGER)' )

def add( user, lolis, act = 0 ):
  """Insert new user in database"""

  #Gets current time
  thetime = time.time()

  action = 'INSERT INTO lolis VALUES ("{}", "{}"'.format( user, lolis )

  if act == 0:
    action += ', "{}", "1"'.format( thetime )
  if act == 1:
    action += ', "1", "{}"'.format( thetime )

  action += " )"

  #Insert user data into table
  cur.execute( action )

def update( user, lolis, act = 0 ):
  """Updates user data"""

  #Gets current time
  thetime = int(time.time())

  action = 'UPDATE lolis SET lolis = "{}"'.format( lolis )

  if act == 0:
    action += ", time = {}".format( thetime )
  if act == 1:
    action += ", stime = {}".format( thetime )

  action += ' WHERE user = "{}"'.format( user )

  #Find user and update loli count and timestamps
  cur.execute( action )

def load( user ):
  """Loads user data"""

  cur.execute('SELECT lolis, time, stime FROM lolis WHERE user="{}"'.format(user))

  #Fetch all data from our querie
  data = cur.fetchone()

  return data

def loli( user ):

  #Interval between command in seconds
  #6 hours should be sane interval
  interval = 3600

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
  output = "{} +{} lolis [TOT: {}]".format( user, newlolis, lolis)

  #Save data
  if mode == 0:
    #Insert new user
    add( user, lolis )
  elif mode == 1:
    #Update previous record
    update( user, lolis )

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
  _caller = load( caller ) # [ lolis, !loli timestamp, !steal timestamp ]
  _target = load( target )

  if not _caller:
    return

  #Target has no lolis
  if not _target:
    return

  #Interval between command in seconds
  interval = 3600
  thetime   = int(time.time())
  timestamp = int(_caller[2])

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
    add( caller, c_lolis, 1 )
  elif c_mode == 1:
    update( caller, c_lolis, 1)

  if loot <= 0:
    return "{} CAN'T INTO STEALING".format( caller )

  #Save targets data
  if t_mode == 0:
    #shouldn't happen
    add( target, t_lolis, 2 )
  elif t_mode == 1:
    update( target, t_lolis, 2)

  return "{} +{}, {} -{} lolis".format( caller, loot, target, loot )

def top( limit = 5, order = "DESC" ):

  cur.execute( 'SELECT user, lolis FROM lolis ORDER BY lolis {} LIMIT {}'.format( order, limit ) )

  data = cur.fetchall()

  return data

def top5():

  interval = 600
  thetime  = int(time.time())
  
  global last_top
  
  if last_top:
    if( ( thetime - last_top ) < interval ):
      return

  last_top = int(time.time())

  return top( 5, "DESC" )

if __name__ == "__main__":
  open()
  create()
  print loli("fatapaca")
  print loli("makos")
  print steal("fatapaca", "makos")
  print steal("makos", "fatapaca")
  print top5()
  save()

