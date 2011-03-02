#!/usr/bin/env python2

import random
import re

eightballdb = ("Yes, {}.", "No, {}.", "Who knows?", "Maybe, {}.", "How should I know?", "That's very possible, {}.", "How about no.", "42.", \
             "No, you piece of shit.", "{} no ecchi!")

def eightball( user ):
    """See the future."""

    return random.choice(eightballdb).format(user)

if __name__ == '__main__':
	print eightball( "fatapaca" )
