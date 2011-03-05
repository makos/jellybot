#!/usr/bin/env python2

import urllib, re

def open(*what):

    print "Searching gelbooru for", repr(what).strip("(',)")

    if len(repr(what).strip("(',)")) > 0:
        url = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=%s&limit=1' % what
    else:
        url = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=infinite_stratos&limit=1'

    content = urllib.urlopen(url)
    images = content.readlines()
    imgs = str(images).split()
    link = re.search("'id.*", str(imgs))

    if imgs:
        try:
            img = link.group().split()
        except AttributeError:
            return "No such tag."

    _len = len(repr(what).strip("(',)"))

    if _len > 0:
        return "Latest image under {}: http://gelbooru.com/index.php?page=post&s=view&id={}".format( str(what).strip("'(),"), img[0].strip("id=\"\\',"))
    else:
        return "Latest image under tag infinite_stratos: http://gelbooru.com/index.php?page=post&s=view&id={}".format(img[0].strip("id=\"\\',"))
