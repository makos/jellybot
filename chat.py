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

    print "Learning:", text

    learn( text )

    return "{}: {}".format( user, reply( text ) )

if __name__ == '__main__':
    print parse( "Hello" )
    print parse( "My name is Jellybot" )
