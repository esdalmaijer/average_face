# -*- coding: utf-8 -*-

import os
import copy
from urllib import urlretrieve
from urllib2 import urlopen


# # # # #
# CONSTANTS

# URL for the Experimental Psychology website
EPURL = u"http://www.psy.ox.ac.uk/team"

# Name for the folder in which face images need to be stored
DIR = os.path.dirname(os.path.abspath(__file__))
FACEDIR = os.path.join(DIR, u'scraped_faces')


# # # # #
# INITIALISE

# Check if the face directory already exists, and make a new one if it doesn't.
if not os.path.isdir(FACEDIR):
	os.mkdir(FACEDIR)

# Read the EP website.
print(u"Reading '%s'" % EPURL)
resp = urlopen(EPURL)
html = resp.read()
# Unicodify the loaded html text.
html = html.decode(u'utf-8')


# # # # #
# FIND NAMES

# Try to detect all the names from the website's HTML code.
# First, we split the html in separate lines.
lines = html.split(u'\n')

# Then we go through all the lines, trying to find the things that typically
# signal a link to a face image. Links to personal profiles occur in the
# following format:
#
#            <a href="http://www.psy.ox.ac.uk/team/firstname-lastname" title="Firstname Lastname">
#                <img data-src="http://www.psy.ox.ac.uk/team/firstname-lastname/@@images/image/64x64" alt="Firstname Lastname" class="lazyload img-responsive img-thumbnail" />
#                
#            </a>
#
# To detect this, we go through all lines, and find all lines that contain
# '<img data-src="http://www.psy.ox.ac.uk/team/' AND '@@images/image/64x64'.
# Then, we simply select the bit between these two snippets, which should be
# 'firstname-lastname/'.
names = []
imgurlstart = u'<img data-src="http://www.psy.ox.ac.uk/team/'
imgurlend = u'/@@images/image/64x64'
for l in lines:
	if imgurlstart in l and imgurlend in l:
		si = l.find(imgurlstart) + len(imgurlstart)
		ei = l.find(imgurlend)
		names.append(copy.deepcopy(l[si:ei]))


# # # # #
# COPY PHOTOS

# Each photo's URL is a reference to the personal image that contains the
# employee's name. This is the generic format:
# 'http://www.psy.ox.ac.uk/team/firstname-lastname/@@images/image/'
imgurl = u'http://www.psy.ox.ac.uk/team/%s/@@images/image/'

# To scrape all the images, we'll go through all the names, construct the URL
# for the image, and attempt to retrieve the image via the URL.
print(u"Retrieving %d face images." % (len(names)))
for name in names:
	urlretrieve(imgurl % (name), os.path.join(FACEDIR, u'%s.jpg' % (name)))

print(u"Done! Scraped images are now in '%s'." % (FACEDIR))