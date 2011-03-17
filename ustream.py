import urllib2, json, time

last_call = 0
data      = None

def _call(channel):

  global data, last_call

  if (time.time() - last_call) < 60:
    print "Too soon"
    return

  call = "http://api.ustream.tv/json/"
  call += "&subject=channel"
  call += "&uid=%s" % channel
  call += "&command=getinfo"
  call += "&key=0489ED89B2C20CB9A1B3B0B4DC96E5C1"

  output = urllib2.urlopen(call)
  _json = json.load(output)
    
  data      = _json['results']
  last_call = time.time()

def is_on(channel):

  _call(channel)

  status = data['status']

  if status == 'live':
    return True
  
  return False

if __name__ == "__main__":
  
  status = is_on("choroyama")

  if status == True:
    print "Choroyama's broadcast has started, START RIPPING"
    print "Watch at http://www.ustream.tv/channel/choroyama"
