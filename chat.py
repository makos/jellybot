#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re
from cobe.brain import Brain

brain = Brain("jellybot.brain")

def learn( text ):
    return brain.learn(text)

def reply( text ):
    return brain.reply(text).encode('utf-8')

def parse( user, text ):

    msg = text.strip('\"')

    print "Learning:", msg

    learn( msg )

    return "{}: {}".format( user, reply( msg ) )

if __name__ == '__main__':
    print parse( "Hello" )
    print parse( "My name is Jellybot" )
