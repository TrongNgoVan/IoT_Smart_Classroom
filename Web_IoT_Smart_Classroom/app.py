from flask import Flask, request, render_template, jsonify, send_file
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import io
from PIL import Image
import base64
from io import BytesIO

app = Flask(__name__)



# Trang chính
@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
