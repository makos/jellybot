import urllib2, json, time

data = {}

def _call(channel):

  global data
  
  if channel in data:
    if (time.time() - data[channel][0]) < 60:
      print "Too soon"
      return

  call = "http://api.ustream.tv/json/"
  call += "&subject=channel"
  call += "&uid=%s" % channel
  call += "&command=getinfo"
  call += "&key=snip"

  output = urllib2.urlopen(call)
  _json = json.load(output)
  
  #data[channel][0] = "sup"
  data[channel] = (time.time(), _json['results'])
  #print data[channel]
  last_call = time.time()

def is_on(channel):

  _call(channel)
  
  status = None

  if channel in data:
    status = data[channel][1]['status']
    print status

  if status == 'live':
    return True
  
  return False

if __name__ == "__main__":
  
  channels = [ "choroyama", "mogra1", "choroyama", "mogra1" ]

  for channel in channels:
    status = is_on(channel)

    if status == True:
      print "%s's broadcast has started, START RIPPING" % channel
      print "Watch at http://www.ustream.tv/channel/%s" % channel


