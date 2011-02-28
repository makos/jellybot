#!/usr/bin/env python2

import sqlite3
import random
import time

db = sqlite3.connect('lolis.db')

def add ( user, lolis):
	
	#if table not found - create table
	db.execute('''create table lolis(user text, lolis integer, time integer);''')
				
	#Add lolis ( Adds new row )
	#if !user in rows
	db.execute('''insert into lolis values (user, lolis, time);''')
	#elif
	#db.execute('''UPDATE lolis SET lolis = 500, time = 1999 WHERE user = "fatapaca";''')
	print "Added"

def save():
	#Add commit changes
	conn.commit()

	#Close file
	conn.close()
	return

def load( user ):
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




