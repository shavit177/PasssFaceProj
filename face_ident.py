import numpy as np
import cv2

# face_cascade contains info about face shapes and scales in order to detect any face.
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
print(face_cascade)

cap = cv2.VideoCapture(0)


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for (x, y, w, h) in faces:
        print(x, y, w, h)
        roi_gray = gray[y:y+h, x:x+w]  # roi- region of interest- only where the face are.
        img_item = "my-image.png"

        cv2.imwrite(img_item, roi_gray)  # saving single frame of roi_gray as img_item

        # drawing a rectangle around the face:
        color = (255, 0, 0) #BGR
        stroke = 2
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, stroke)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    #  cv2.imshow('gray', gray)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()