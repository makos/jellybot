#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re
from cobe.brain import Brain

brain = Brain("jellybot.brain")

def _learn( text ):
    return brain.learn(text)

def _reply( text ):
    return brain.reply(text).encode('utf-8')

def parse( user, msg, nickname, reply = True, adressed = True ):

    nick = ""
    text = msg

    if msg == None:
        return

    m = re.match( r"^(?P<nick>\S+)[,:] ?(?P<body>.*)", msg )

    if m:
        nick = m.group( "nick" ) #Adress
        text = m.group( "body" ) #Actual text

    #Learn text
    if text:
        _learn( text )
    else:
        return _learn( msg )

    if adressed == False:
        return "{}: {}".format( user, _reply( text ) )
    else:
        if nick == nickname:
            if reply:
                return "{}: {}".format( user, _reply( text ) )

    return
