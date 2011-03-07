import urllib, urllib2
import simplejson
import pprint

baseTranslateUrl = "http://ajax.googleapis.com/ajax/services/language/translate"

def _translate(text, langpair = "ja|en", format='text', v='1.0'):

  params = {'q':text.encode('utf8'),'format':format,'langpair':langpair,'v':v}

  if len(params['q'])>4500:
      return None

  request = urllib2.Request(baseTranslateUrl,data=urllib.urlencode(params))

  request.add_header("Accept-encoding", "gzip")

  resp = simplejson.load(urllib2.urlopen(request))

  output = None

  try:

    output = resp['responseData']['translatedText']

  except:
      print "**************** Error! ****************"
      pprint.pprint(resp)

  return output
