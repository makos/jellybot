#!/usr/bin/env python2

import urllib, re

def open(*what):
    
    if len(repr(what).strip("(',)")) > 0:
        url = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=%s&limit=1' % what 
    else:
        url = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=infinite_stratos&limit=1'
    content = urllib.urlopen(url)
    images = content.readlines()
    imgs = str(images).split()
    link = re.search("http.*", str(imgs))
    if link:
        img = link.group().split()
    if len(repr(what).strip("(',)")) > 0:
        return "Latest image under tag {}: {}".format(str(what).strip("'(),"), img[0].strip("\",'"))
    else:
        return "Latest image under tag infinite_stratos: {}".format(img[0].strip("\",'"))
       #image.split()
        #link = re.search("http.*", image)
        #if link:
            #img = link.group().split()
        #print img[0].strip("\"")
        