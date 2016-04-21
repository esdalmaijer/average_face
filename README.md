Oxford Experimental Psychology Face-Average-O-Matic
---------------------------------------------------

This is a bunch of simple scripts that scrape the Oxford
Experimental Psychology [website](http://www.psy.ox.ac.uk/team) for people's personal photos.
These can be uploaded by each individual member of staff, and by
grad students who are working towards their PhD. There is no
standard format required (I think there might actually be some
rules, but most people seem to ignore them), which means that the
photos need to be automatically processed to find the faces. For
this, I used the Haar cascade algorithm from [@shantnu](https://github.com/shantnu)'s
[FaceDetect](https://github.com/shantnu/FaceDetect) project. After all the faces are detected, they are
averaged, and the resulting image is saved. (And it might haunt
your dreams for years to come.)

Note that not all the faces have the same orientation, so the
averaging is imperfect at best. One solution could be to detect
the eyes, and realign each image to a horizontal eye-line. Have
fun implementing that, and give me a shout (and a pull request,
please) once you're done.


USAGE
-----

1) **Run [extract_faces.py](https://github.com/esdalmaijer/average_face/blob/master/extract_faces.py)**. This will scrape the 'team' part of
the EP website. The html source of this page contains references
to all EP members. This script finds the links to each member's
image, and then downloads those. The downloaded images will be in
a folder called `scraped_faces`.

2) **Run [detect_faces.py](https://github.com/esdalmaijer/average_face/blob/master/detect_faces.py)**. This will go through all the images in
the `scraped_faces` folder, and it will attempt to detect any
faces in those images. Note that it can detect multiple faces per
image, and that it can make mistakes every now and again. The
detected faces are cropped, and the resulting images are stored
in a folder called `detected_faces`.

3) Manually check the faces. This step is a manual one, because
humans are waaaaaaay better at detecting faces than computers
are. **Create a folder called `filtered_faces`, and copy all the
images from `detected_faces` that actually contain a face**.

4) **Run [average_face.py](https://github.com/esdalmaijer/average_face/blob/master/average_faces.py)**. This will load all images in the
`filtered_faces` folder, and it will then calculate the average
face. This will be stored as `EP_average_face.jpg`.