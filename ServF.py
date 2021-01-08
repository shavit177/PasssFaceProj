import socket
import threading
import numpy as np
import cv2
import os
import pickle

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")
class Server(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.count = 0

    def start(self):
        try:
           print('server starts up on ip %s port %s' % (self.ip, self.port))
           # Create a TCP/IP socket
           sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           sock.bind((self.ip, self.port))
           sock.listen(3)

           while True:
                print('waiting for a new client')
                # block
                clientSocket, client_address = sock.accept()

                print('new client entered')

                # send receive example
                clientSocket.sendall('Hello this is server'.encode())
                msg = clientSocket.recv(1024)
                print('received message: %s' % msg.decode())
                self.count += 1
                print(self.count)
                # implement here your main logic
                self.handleClient(clientSocket, self.count)
        except socket.error as e:
            print(e)

    def handleClient(self, clientSock, current):
        print ("hello")
        client_handler = threading.Thread(target=self.handle_client_connection, args=(clientSock, current,))
        # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
        client_handler.start()

    def handle_client_connection(self, client_socket, current):
        send_file(client_socket, "trainner.yml")
        set_labels(client_socket)
        while True:
            print("start")
            try:

                getting_image(client_socket)
            except:
                print("1111")
                continue


def set_labels(client_socket):
    labels = {}
    with open("labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v: k for k, v in og_labels.items()}
    print(labels)
    for i in labels:
         client_socket.send(str(labels[i]).encode())
    client_socket.send("-1".encode())


def getting_image(client_socket):
    data = client_socket.recv(1024)
    print(data)
    filesize = int((data).decode())
    print(filesize)
    f = open('ser_' + "img.jpg", 'wb')
    data = client_socket.recv(1024)
    if data != "-1":
        totalrecv = int(len(data))
        print(totalrecv)
        f.write(data)
        while totalrecv < filesize:
            data = client_socket.recv(1024)
            totalrecv += len(data)
            f.write(data)
            print("{0:.2f}".format((totalrecv / float(filesize)) * 100) + "% done")
        print("download complete")
        f.close()
        print('Received {}')

def send_file(client_socket, filename):
    f = open(filename, 'rb')
    l = f.read(1024)
    while (l):
        client_socket.send(l)
        print('Sent ', repr(l))
        l = f.read(1024)
    f.close()

    print('Done sending')

def delete_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        print("successfully deleted")
    else:
        print("The file does not exist")

if __name__ == '__main__':
   ip = '0.0.0.0'
   port = 1730
   s = Server(ip, port)
   s.start()
