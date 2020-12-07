import cv2
import numpy as np
import os
from PIL import Image
import pickle

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()


BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # looking for the path of the file
image_dir = os.path.join(BASE_DIR, "pictures") # directing the path to the pictures file

current_id = 0
labels_ids = {}
y_labels = []
x_train = []

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith(".png") or file.endswith(".jpg"):  #only the path of jpg and png files
            path = os.path.join(root, file)
            #  labeling the images, replacing " " and only lowercase letters
            label = os.path.basename(os.path.dirname(path)).replace(" ", "-").lower()
            print(label, path)
            # turn the picture into NUMPY array
            pil_image = Image.open(path).convert("L")  #grayscale
            image_array = np.array(pil_image, "uint8")
            print(image_array)
            if label not in labels_ids:
                labels_ids[label] = current_id
                current_id += 1
            id_ = labels_ids[label]
            faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

            for (x, y, w, h) in faces:
                roi = image_array[y:y+h, x:x+w]  # walking through only where the face are
                x_train.append(roi)
                y_labels.append(id_)

# print(labels_ids)
# print(y_labels)
# print(x_train)

with open("labels.pickle", 'wb')as f:
    pickle.dump(labels_ids, f)

recognizer.train(x_train, np.array(y_labels))
recognizer.save("trainer.yml")
