import urllib2, os, json, time

from BeautifulSoup import BeautifulSoup
from chan_utils import *

class Thread(object):
  def __init__(self, board, thread):
    self.board     = board
    self.thread    = thread
    self.url       = "http://boards.4chan.org/%s/res/%s" % ( board, thread )
    self.posts     = []
    self.postcount = 0
    self.images    = 0
    return

  def __repr__(self):
    return "Thread with %s posts and %s images" % ( self.postcount, self.images )

  def add_post(self, post):
    if post.image.filename:
      self.images += 1

    self.postcount += 1

    return self.posts.append(post)

  def del_post(self, id):
    return

  def get_posts(self):
    return self.posts
  
  def _posts():
    return self.postcount

  def _images():
    return self.images

  def save(self):

    target = os.path.join(self.board, self.thread, "thread.js")
    
    posts = []
    dump  = {}

    dump['board']      = self.board
    dump['thread']     = self.thread
    dump['url']        = self.url
    dump['post_count'] = self.postcount
    dump['images']     = self.images 

    dump['posts']     = posts

    for post in self.posts:
      posts.append({
        'id'         : post.id,
        'time'       : post.time,
        'poster'     : post.poster,
        'email'      : post.email,
        'trip'       : post.trip,
        'text'       : post.text,
        'img_name'   : post.image.filename,
        'img_title'  : post.image.title,
        'img_size'   : post.image.size,
        })

    with open(target, 'w') as f:
      json.dump(dump, f)
    
    return

class Post(object):
  def __init__(self, id, text, poster, email, trip, timestamp, image):
    self.id     = id
    self.time   = timestamp

    self.poster = poster
    self.email  = email
    self.trip   = trip

    self.text   = text

    self.image = image
    
    return

  def __repr__(self):
    if self.image.filename:
      return u"%s by %s with %s" % (self.id, self.poster, self.image.filename)
    else:
      return u"%(id)s by %(poster)s with no image" % self.__dict__

class Image(object):
  url      = None
  filename = None
  title    = None
  size     = None
  width    = None
  height   = None

  def __init__(self, data):
    if not data:
      return

    self.url      = data[0]
    self.filename = data[1]
    self.title    = data[2]
    self.size     = data[3]
    self.width    = data[4]
    self.height   = data[5]
    return

def parse_thread( board, thread):

  url = "http://boards.4chan.org/%s/res/%s" % ( str(board), str(thread) )

  print "Parsing thread %s from board /%s/ at %s" % ( thread, board, url )
  
  html = urllib2.urlopen(url)

  soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)

  html.close()

  thread = Thread( board, thread )
  replies = soup.findAll('td', {"class": "reply"})

  for td in replies:
    thread.add_post(parse_post(td, thread))

  return thread


def parse_post(node, thread):
  #Author
  name  = get_name(node)
  email = get_email(node)
  trip  = get_trip_code(node)

  #Post
  id      = get_id(node)
  subject = get_subject(node)
  text    = get_text(node)
  
  #Image
  image = Image(get_img_data(node))

  post = Post(id, text, name, email, trip, 0, image)

  return post

def download_images(thread):
  interval  = 0
  overwrite = False

  base = os.path.join(thread.board, thread.thread, "images")

  if not os.path.exists(base):
    os.makedirs(base)

  for post in thread.posts:
    if post.image.filename:
      path = os.path.join(base, post.image.filename)
      
      if os.path.exists(path):
        if not overwrite and os.path.getsize(path) != 0:
          continue
        
      print u"downloading %s to %s" % (post.image.url, post.image.filename)

      with open(path, 'w') as f:
        try:
          remote = urllib2.urlopen(post.image.url)
        except urllib2.HTTPError, e:
          if e.code == 404:
            print "image 404ed"
          raise
        
        f.write(remote.read())
      
    time.sleep(interval) # be nice to the servers
  
  return

if __name__ == "__main__":
  board = "a"
  thread = "47004373"

  thread = parse_thread( board, thread )

  download_images(thread)

  thread.save()

