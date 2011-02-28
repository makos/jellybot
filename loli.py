#!/usr/bin/env python2

import sqlite3
import random
import time

db = sqlite3.connect('lolis.db')

def add ( user, lolis):
	#Create table
	#db.execute('''create table lolis(user text, lolis text)''')
				
	#Add lolis
	db.execute('''insert into lolis(user) lolis ''')
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




