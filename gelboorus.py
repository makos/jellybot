#!/usr/bin/env python2

import urllib, re

def search(tag):
	_tag = str(tag).strip("('),")
	print "Searching for tag", _tag.strip("(',)")

	return "Gelbooru search for tag", _tag, " returned these results: http://gelbooru.com/index.php?page=post&s=list&tags={}".format(_tag)
