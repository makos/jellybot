#!/usr/bin/env python2

import urllib, re

def search(tag):

  print "Searching for tag", tag

  output = "Gelbooru search for tag {}: http://gelbooru.com/index.php?page=post&s=list&tags={}".format(tag, tag.replace(" ", "+"))

  return output

if __name__ == "__main__":
  search(["niggers"])
