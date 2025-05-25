# USAGE
# python liveness_demo.py

# import the necessary packages
from imutils.video import VideoStream
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import os
import urllib.request
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;0"

# Cài đặt các tham số đầu vào
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", type=str, default='liveness.model.h5',  # Đổi tên file ở đây
                help="path to trained model")
ap.add_argument("-l", "--le", type=str, default='le.pickle',
                help="path to label encoder")
ap.add_argument("-d", "--detector", type=str, default='face_detector',
                help="path to OpenCV's deep learning face detector")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
                help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# Load model nhận diện khuôn mặt
print("[INFO] loading face detector...")
protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"],
                              "res10_300x300_ssd_iter_140000.caffemodel"])
net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

# Load model nhận diện fake/real
print("[INFO] loading liveness detector...")
model = load_model(args["model"])  # Đảm bảo rằng file model là .h5
with open(args["le"], "rb") as f:
    le = pickle.load(f)

# Đọc video từ webcam
print("[INFO] starting video stream...")
url = 'http://192.168.43.181/cam-mid.jpg'
while True:
    try:
        # Fetch image frame from ESP32-CAM
        img_resp = urllib.request.urlopen(url)
        img_np = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_np, -1)

        # Resize the frame to improve performance
        frame = cv2.resize(frame, (600, 400))  # Resize frame

        # Convert the frame to blob for face detection
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                     (300, 300), (104.0, 177.0, 123.0))

        # Detect faces
        net.setInput(blob)
        detections = net.forward()

        # Loop over detected faces
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            # If confidence is higher than threshold, process the face
            if confidence > args["confidence"]:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                startX = max(0, startX)
                startY = max(0, startY)
                endX = min(w, endX)
                endY = min(h, endY)

                # Get the face region
                face = frame[startY:endY, startX:endX]
                if face.shape[0] == 0 or face.shape[1] == 0:
                    continue  # Skip if no valid face region

                face = cv2.resize(face, (32, 32))
                face = face.astype("float") / 255.0
                face = img_to_array(face)
                face = np.expand_dims(face, axis=0)

                # Use model to predict real/fake
                preds = model.predict(face)[0]

                j = np.argmax(preds)
                label = le.classes_[j]

                # Draw bounding box around face
                label = "{}: {:.4f}".format(label, preds[j])
                color = (0, 255, 0) if j == 1 else (0, 0, 255)
                cv2.putText(frame, label, (startX, startY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        # Show frame with detected faces and liveness prediction
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # Press 'q' to exit
        if key == ord("q"):
            break

    except Exception as e:
        print(f"Error fetching frame: {e}")
        break

# Cleanup
cv2.destroyAllWindows()

