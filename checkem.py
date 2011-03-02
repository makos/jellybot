#!/usr/bin/env python2

import random
import time

dict = ("{0}. Pffft, try harder next time.",  "Seriously? {0}? Are you kidding me?", "{0}. You suck.", "Keikaku doori. You failed. {0}.", "Only bakas get {0}.")

last_usage = 0
doubles = ('00', 11, 22, 33, 44, 55, 66, 77, 88, 99)


def checkem( user ):
    """Check those dubs."""

    output = ""
    number = random.randint(00, 99)

    global channel, last_usage

    #Wait five seconds before actually doing anything
    if (int(time.time()) - last_usage) < 5:
        if random.randint(0, 3) == 0:
            output = "Calm down, {}.".format( user )

        return output

    if number in doubles:
        output = "CHECK EM! {} rolled {}".format( user, number )

    elif random.randint(0, 1):
        output = random.choice(dict).format(number)
        return output
        #self.server.kick(channel, user)
        #print "KICKED:", user

    #Log last usage time
    last_usage = int(time.time())

    return output

if __name__ == '__main__':
    output = checkem( "fatapaca" )

    if output:
        print output

