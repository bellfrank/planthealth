import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, url_for

from helpers import apology, login_required, lookup, usd, contrast_stretch, calc_ndvi, fastiecm

import numpy as np
import cv2


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_PATH'] = 'static/uploads'

# Configure CS50 Library to use SQLite database

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":

        # getting user uploaded image and saving to static/uploads
        images = []
        file = request.files['file']
        images.append(file.filename)

        file.save(os.path.join(app.config['UPLOAD_PATH'], file.filename))

        # getting path to image to read into variable original 
        # getting the full path will be an issue for later to come ?????
        
        original = cv2.imread(f'/Users/joserodriguez/Desktop/SOLO LEARN/plant health/ndvi/static/uploads/{file.filename}')
        
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
        
        cv2.imwrite(f'/Users/joserodriguez/Desktop/SOLO LEARN/plant health/ndvi/static/uploads/{contrast}', contrasted)
        images.append(contrast)

        cv2.imwrite(f'/Users/joserodriguez/Desktop/SOLO LEARN/plant health/ndvi/static/uploads/{ndvi_image}', ndvi)
        images.append(ndvi_image)

        cv2.imwrite(f'/Users/joserodriguez/Desktop/SOLO LEARN/plant health/ndvi/static/uploads/{contrast_ndvi_image}', contrast_ndvi)
        images.append(contrast_ndvi_image)

        cv2.imwrite(f'/Users/joserodriguez/Desktop/SOLO LEARN/plant health/ndvi/static/uploads/{color_mapped_image_path}', color_mapped_image)
        images.append(color_mapped_image_path)

        return render_template('modified.html', images=images)
        
    else:
        return render_template('layout.html')
