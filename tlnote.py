#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time, sqlite3, random

global db, cur

def _open():

  global db, cur

  db  = sqlite3.connect('tlnote.db')
  cur = db.cursor()
  return

def _create():

  cur.execute( 'CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, note TEXT, user TEXT, time INTEGER)' )

  return

def _close():

  #Commit changes
  db.commit()

  #Close everything
  cur.close()
  db.close()

  return

def _insert( user, note ):

  cur.execute( 'INSERT INTO data VALUES (null, "{}", "{}", {})'.format( note, user, int(time.time()) ) )

  return

def load_total ( ):
  cur.execute( 'SELECT COUNT(*) FROM data' )

  return cur.fetchone()[0]

def load_note ( row ):

  cur.execute('SELECT note, user, time FROM data WHERE id = {}'.format(row))

  return cur.fetchone()

def is_duplicate ( note ):
	cur.execute('SELECT id FROM data WHERE note = "{}"'.format(note))
	note = cur.fetchone()

	if note:
		return True

	return False

def add( user, note ):

  _time = int(time.time())

  if is_duplicate(note):
	  return False

  _insert( user, note )

  return True

def tlnote( id = -1 ):

  total = load_total()

  if total < 1:
    return

  row   = random.randint( 1, total )

  note  = load_note( row )

  if not note:
	  return

  return "TL NOTE: {}".format( note[0] )

if __name__ == '__main__':

  _open()
  _create()

  add( "fatapaca", "Keikaku means plan." )
  add( "fatapaca", "Kuroneko means black cat." )
  print tlnote()

  _close()


