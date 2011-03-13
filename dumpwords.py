import sqlite3, os

def dump(brain):
  db = sqlite3.connect(brain)
  c  = db.cursor()
  
  q = "SELECT text FROM tokens"
  c.execute(q)
	
  f = open("words.txt", 'w')
  
  for word in c.fetchall():
    try:
      print word[0]
      f.write(word[0] + "\n")
    except UnicodeEncodeError, e:
      pass
  
  f.close()
  
  c.close()
  db.close()

if __name__ == "__main__":
  dump("jellybot.brain")
