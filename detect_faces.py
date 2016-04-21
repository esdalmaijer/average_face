# -*- coding: utf-8 -*-

import os

import cv2


# # # # #
# CONSTANTS

# Sizes for the input and the output. The first is the size to which input
# images are rescaled before face detection is attempted, and the second is
# the size to which output images of faces are rescaled. Either can also be set
# to None, which will prevent any rescaling.
INHEIGHT = 600
OUTHEIGHT = 300

# Name for the folder in which face images need to be stored
DIR = os.path.dirname(os.path.abspath(__file__))
FACEDIR = os.path.join(DIR, 'scraped_faces')
DETECTDIR = os.path.join(DIR, 'detected_faces')

# Path to the Haar Cascade file.
CASCPATH = os.path.join(DIR, 'haarcascade_frontalface_default.xml')


# # # # #
# INITIALISE

# Check if the source directory exists, and raise an Exception if it doesn't.
if not os.path.isdir(FACEDIR):
	raise Exception("ERROR! Source directory does not exist. Expected to find '%s'" % FACEDIR)

# Check if the face directory already exists, and make a new one if it doesn't.
if not os.path.isdir(DETECTDIR):
	os.mkdir(DETECTDIR)

# Create the haar cascade.
face_cascade = cv2.CascadeClassifier(CASCPATH)


# # # # #
# DETECT

# For the detection of faces in EP's employee photos, we'll use a Haar cascade.
# This is defined in the attached xml document, kindly provided by Shantu
# Tiwari. Read https://realpython.com/blog/python/face-recognition-with-python/
# for more information on the specific algorithm. You can also download
# @shantnu's GitHub repo: https://github.com/shantnu/FaceDetect/

# Loop through all the image files.
imgnames = os.listdir(FACEDIR)
print("Found %d source images." % len(imgnames))

# Loop through all the image files.
for imgname in imgnames:
	
	# Construct the path to the image.
	imgpath = os.path.join(FACEDIR, imgname)

	# Try to read the image, and produce a warning if it's impossible.
	# (Some images from the EP website cannot be downloaded; probably due to
	# the original being a weird file type)
	try:
		image = cv2.imread(imgpath)
		grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	except:
		# Print a warning, and skip further processing of this image.
		print("WARNING! Could not process image '%s'" % imgname)
		continue
	
	# Optionally rescale the image.
	if INHEIGHT != None:
		h, w = grey.shape
		scale = INHEIGHT / float(h)
		grey = cv2.resize(grey, (int(w*scale), int(h*scale)))
	
	# Detect faces in the image.
	faces = face_cascade.detectMultiScale(
	    grey,
	    scaleFactor=1.1,
	    minNeighbors=5,
	    minSize=(100, 100),
	    flags = cv2.cv.CV_HAAR_SCALE_IMAGE
	)
	
	# If one or more faces are detected, loop through the rectangles that
	# contain the faces.
	for i in range(len(faces)):
		# Get the face rect.
		x, y, w, h = faces[i]
		# Construct a name and a path for the cropped face image.
		name, ext = os.path.splitext(imgname)
		facepath = os.path.join(DETECTDIR, '%s-%d%s' % (name, i, ext))
		# Crop the face's part of the image.
		crop = grey[y: y + h, x: x + w]
		# Rescale the cropped image to the preferred output size.
		if INHEIGHT != None:
			h, w = crop.shape
			scale = INHEIGHT / float(h)
			crop = cv2.resize(crop, (int(w*scale), int(h*scale)))
		# Store the face as a new image.
		cv2.imwrite(facepath, crop)

print("Detected %d faces!" % len(os.listdir(DETECTDIR)))
