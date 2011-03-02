#!/usr/bin/python2

import urllib
import simplejson

def query( what ):

    query = urllib.urlencode({'q' : what})

    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)

    search_results = urllib.urlopen(url)
    json = simplejson.loads(search_results.read())

    return json['responseData']['results']

def search( user, what ):

    print "Searching for", what

    results = query( what )

    """ Prints all results
    for i in results:
        print i['title'] + ": " + i['url']
    """

    if results:
        return "{}, your search returned: {} @ {}".format( user, results[0]['title'],  results[0]['url'])

    return "{}, I couldn't find anything about {}".format( user, str(what) )

if __name__ == "__main__":
    print search("fatapaca", "lolis")
git pul
