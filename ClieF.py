import socket
import numpy as np
import cv2
import os
from PIL import Image
import threading

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

cap = cv2.VideoCapture(0)
class Client (object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def start(self):
        try:
            print('connecting to ip %s port %s' % (ip, port))
            # Create a TCP/IP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            print('connected to server')
            # send receive example
            msg = sock.recv(1024)
            print('received message: %s' % msg.decode())
            sock.sendall('Hello this is client, send me a job'.encode())
            #implement here your main logic
            while True:
                self.handleServerJob(sock)
        except socket.error as e:
            print(e)

    def handleServerJob(self, serverSocket):
        labels = {}
        t1 = threading.Thread(target=getting_file(serverSocket, "Ctrainner.yml"))
        t2 = threading.Thread(target=set_labels(serverSocket, labels))
        #getting_file(serverSocket, "Ctrainner.yml")
        t1.start()
        recognizer.read("Ctrainner.yml")
        t2.start()
        print(labels)
        #labels = set_labels(serverSocket)
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

            for (x, y, w, h) in faces:
                print(x, y, w, h)
                roi_gray = gray[y:y + h, x:x + w]  # roi- region of interest- only where the face are.
                img_item = "my-image.png"
                cv2.imwrite(img_item, roi_gray)  # saving single frame of roi_gray as img_item

                id_, conf = recognizer.predict(roi_gray)
                if conf >= 45 and conf <= 85:
                    print("welcome " + labels[id_])
                    delete_file("Ctrainner.yml")
                else:
                    print("permission denied")
                print(conf)

                print(os.path.getsize(img_item))
                # drawing a rectangle around the face:
                color = (255, 0, 0)  # BGR
                stroke = 2
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, stroke)

                cap.release()
                cv2.destroyAllWindows()
                send_image(img_item, serverSocket)
                break



            # Display the resulting frame
            print("out")
            cv2.imshow('frame', frame)

            #  cv2.imshow('gray', gray)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break



        print("out")
        cap.release()
        cv2.destroyAllWindows()


def isEmpty(dictionary):
    for element in dictionary:
        if element:
            return False
        return True


def set_labels(server_socket, labels):
    data = (server_socket.recv(1024)).decode()
    while data != "-1":
        i = 0
        labels[i] = data
        print(data)
        i += 1
        data = (server_socket.recv(1024)).decode()
    print(labels)



def send_image(img_item, serverSocket):
    serverSocket.send(str(os.path.getsize(img_item)).encode())

    with open(img_item, 'rb') as f:
        byte_to_send = f.read(1024)
        serverSocket.send(byte_to_send)
        while byte_to_send != "":
            byte_to_send = f.read(1024)
            serverSocket.send(byte_to_send)

def getting_file(serverSocket, filename):
    with open(filename, 'wb') as f:
        print('file opened')
        while True:
            print('receiving data...')
            data = serverSocket.recv(1024)
            print('data=%s', data)
            # write data to a file
            f.write(data)
            if len(data) < 1024:
                break
    f.close()
    print('Successfully get the file')




def delete_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        print("successfully deleted")
    else:
        print("The file does not exist")


if  __name__ == '__main__':
    ip = '127.0.0.1'
    port = 1730
    c =Client(ip, port)
    c.start()