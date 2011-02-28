#!/usr/bin/env python2

import sqlite3
import random
import time

db = sqlite3.connect('lolis.db')
cur = db.cursor()

def add ( user, lolis):
	
	thetime = time.time()
	
	#if table not found - create table
	#cur.execute( 'CREATE TABLE lolis (user TEXT, lolis INTEGER, time INTEGER)' )
				
	#Add lolis ( Adds new row )
	#if !user in rows
	#Will always add new row
	cur.execute( 'INSERT INTO lolis VALUES (?, ?, ?)', ( user, lolis, int(thetime) ) )

	#elif
	cur.execute( 'UPDATE lolis SET lolis = ?, time = ? WHERE user = ?', (lolis, int(thetime), user  ))
	db.commit()
	print "Added"

def load( user ):
	# Y WON'T U WORK
	cur.execute( 'SELECT * FROM lolis WHERE user = ?', user )
	print cur.fetchall()
	return

def loli( user, time):
	
	last_usage = time
	interval = 3600

	min_lolis = 0
	max_lolis = 10

	#Load data?
	load( user )

	if( (time - last_usage) > interval ):
		print "Calm down, bro"
		return
	
	lolis = random.randint( min_lolis, max_lolis)

	print user, "got", lolis, "lolis!"
	add( user, lolis )

if __name__ == "__main__":
	loli("fatapaca", time.time())
	#loli("makos", time.time())




