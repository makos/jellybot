#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time
#import datetime

lastu = 0

def formats( seconds ):

    days    = seconds / 86400
    seconds -= 86400 * days
    hours   = seconds / 3600
    seconds -= 3600 * hours
    minutes = seconds / 60
    seconds -= 60 * minutes

    if days == 0:
        if hours == 0:
            return "%02d:%02d" % ( minutes, seconds )

        return "%02d hours %02d minutes %02d seconds" % ( hours, minutes, seconds )

    return "%02d days %02d hours %02d minutes %02d seconds" % ( days, hours, minutes, seconds )

    #return str(datetime.timedelta(seconds=time))

def timeleft( user ):
    airtime     = float(1299169500)
    currenttime = time.time()
    remaining   = int(airtime - currenttime)

    global lastu

    if (int(currenttime) - lastu) < 5:
        return ""

    #If airtime is outdated
    while remaining <= 0:
        print "WARNING: [timeleft] Airing date outdated! Adding one week!"
        #Add one week
        remaining += 604800

    lastu = currenttime

    return "{}, {} until next episode. It can't come soon enough, ne?".format( user, formats(remaining) )

if __name__ == '__main__':
    print timeleft( "fatapaca" )
    print timeleft( "fatapaca" )
    print timeleft( "fatapaca" )
    print timeleft( "fatapaca" )
    print timeleft( "fatapaca" )

