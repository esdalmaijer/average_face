import os

import numpy
from scipy.misc import imread, imsave


# # # # #
# CONSTANTS

# Size of the images that will be loaded.
IMGSIZE = (600, 600)

# Name for the folder in which face images are stored.
DIR = os.path.dirname(os.path.abspath(__file__))
FACEDIR = os.path.join(DIR, 'filtered_faces')
OUTFILE = os.path.join(DIR, 'EP_average_face.jpg')


# # # # #
# LOAD FACES

# Get a list of all face image names.
imgnames = os.listdir(FACEDIR)

# Create a matrix that can contain all images.
imgmatshape = (IMGSIZE[1], IMGSIZE[0], len(imgnames))
imgmat = numpy.zeros(imgmatshape)

# Loop through all images, and load them into the image matrix.
for i in range(len(imgnames)):
	# Load the image.
	img = imread(os.path.join(FACEDIR, imgnames[i]))
	# Reshape the image to the correct size.
	img.resize(IMGSIZE)
	# Store a copy of the image in the image matrix.
	imgmat[:,:,i] = numpy.copy(img)

# Average all the faces.
avgimg = numpy.mean(imgmat, axis=2)

# Save the image.
imsave(OUTFILE, avgimg)