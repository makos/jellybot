#!/usr/bin/env python2

import twitter
import gtranslate

api = twitter.Api()

def stalk( name = "choroyama", num = 5, start = None):

  tweets = api.GetUserTimeline(screen_name=name, count=num, since_id=start)

  return tweets

if __name__ == "__main__":

  tweets = stalk()

  for s in tweets:
    print "D-YAMA: %s [Posted %s.]" % (s.text, s.relative_created_at )
    print ">> Engrish: %s" % ( gtranslate._translate(s.text) )
