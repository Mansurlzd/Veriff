import base64
import scipy
import tensorflow as tf
import cv2
import numpy as np
import os
from PIL import Image
from flask import Flask, render_template, request, make_response
from facenet.src.align import detect_face
from skimage.io import imsave

PEOPLE_FOLDER = os.path.join('static', 'people_photo')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
@app.route('/')
def hello_world():
    return render_template('index.html')

#https://github.com/davidsandberg/facenet/blob/master/tmp/mtcnn.py
def getBoundingBoxes(img, minsize, threshold, factor):

    with tf.Graph().as_default():
        sess = tf.Session()
        with sess.as_default():
            pnet, rnet, onet = detect_face.create_mtcnn(sess, None)
            bounding_boxes, points= detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
            for (x1, y1, x2, y2, acc) in bounding_boxes:
                rectangle = cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

            return rectangle,bounding_boxes


@app.route("/getResult", methods=['POST'])
def getResult():

    minsize = 20  # minimum size of face
    threshold = [0.6, 0.7, 0.7]  # three steps's threshold
    factor = 0.709  # scale factor
#get the image from form
    image = request.files['image']
    img_str = image.read()
    #print(type(img_io))
#https://stackoverflow.com/questions/17170752/python-opencv-load-image-from-byte-string
    nparr = np.fromstring(img_str, np.uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    rectangle, bounding_boxes = getBoundingBoxes(cv2_img, minsize, threshold, factor)



    if request.method=='POST' and bounding_boxes.size != 0:
        points, buffer = cv2.imencode('.png', rectangle)

        # Convert to base64 encoding and show start of data
        jpg_as_text = base64.b64encode(buffer)
        print(jpg_as_text[:80])

        # Convert back to binary
        jpg_original = base64.b64decode(jpg_as_text)

        # Write to a file to show conversion worked
        with open(PEOPLE_FOLDER, 'wb') as final_output:
            final_output.write(jpg_original)
        #hardcoded
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'test.jpg')
        return render_template('result.html',user_image = full_filename,bounding_boxes=int(bounding_boxes.size/5))

if __name__ == '__main__':
    app.run()
