import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for

from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.utils import secure_filename

from flask_session import Session

from helpers import apology, contrast_stretch, calc_ndvi, fastiecm

import numpy as np
import cv2
from time import sleep

UPLOAD_PATH = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Configure application
app = Flask(__name__)

# # Ensure responses aren't cached
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_PATH'] = UPLOAD_PATH


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            # flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

            # getting user uploaded image and saving to static/uploads
            images = []
            images.append(filename)
            
            original = cv2.imread(f'static/uploads/{file.filename}')
            
            # sending original image through contrast and saving
            contrasted = contrast_stretch(original)
            
            ndvi = calc_ndvi(contrasted)
            contrast_ndvi = contrast_stretch(ndvi)

            color_mapped_prep = contrast_ndvi.astype(np.uint8)
            color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)


            contrast = 'contrast.' + file.filename.rsplit('.', 1)[1].lower()
            ndvi_image = 'nvdi.' + file.filename.rsplit('.', 1)[1].lower()
            contrast_ndvi_image ='contrast_ndvi.' + file.filename.rsplit('.', 1)[1].lower()

            color_mapped_image_path = 'color_mapped.' + file.filename.rsplit('.', 1)[1].lower()
            
            cv2.imwrite(f'static/uploads/{contrast}', contrasted)
            images.append(contrast)

            cv2.imwrite(f'static/uploads/{ndvi_image}', ndvi)
            images.append(ndvi_image)

            cv2.imwrite(f'static/uploads/{contrast_ndvi_image}', contrast_ndvi)
            images.append(contrast_ndvi_image)

            cv2.imwrite(f'static/uploads/{color_mapped_image_path}', color_mapped_image)
            images.append(color_mapped_image_path)

            return render_template('modified.html', images=images)
    return render_template('index.html')


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)