#!/usr/bin/python2

import urllib
import simplejson
import re

def query( what ):

    query = urllib.urlencode({'q' : what})

    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)

    search_results = urllib.urlopen(url)
    json = simplejson.loads(search_results.read())

    return json['responseData']['results']

def search( user, what ):

    print "Searching for", what

    results = query( what )

    if results:
        title = results[0]['title'].encode('utf8')
        title = re.sub("</?b>", "", title)

        url = results[0]['url'].encode('utf8')

        return "{}, your search returned: {} @ {}" .format( user, title, url )

    return "{}, I couldn't find anything about {}".format( user, what )

