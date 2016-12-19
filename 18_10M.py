# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 07:44:23 2016

@author: nikkiemashian

Assignment 10M
"""
# -*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QTextEdit
from PyQt4.QtCore import QTimer
import threading
import sys
import socket

class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.i = 0
        self.setup_window()
        t = threading.Thread(target=self.setup_networking)
        t.start()
        
    def setup_window(self):
        self.setWindowTitle("Chat app")
        self.setGeometry(100,100,400,300)
        
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.label = QLabel(self)
        self.textbox = QLineEdit(self)
        self.textbox.setReadOnly(True)
        
        self.layout2 = QHBoxLayout(self)
        
        self.chathistory = QTextEdit(self) 
        self.chathistory.setReadOnly(True)
        
        self.widget2 = QWidget()
        self.widget2.setLayout(self.layout2)
        
        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.chathistory)
        self.layout2.addWidget(self.label)

        self.layout.addWidget(self.widget2)
        
        #first it'll try to be client and fail. So it will be server. Next time it'll be client
#
#        t3=threading.Thread(target=self.be_client)
#        t3.start()
#        t4=threading.Thread(target=self.be_server)
#        t4.start()        
    def setup_networking(self):
        try:
            self.be_client()  
        except:
            print "unable to connect as client, opening server mode:\n"
            self.be_server()   
            
        self.textbox.setReadOnly(False)
        t2 = threading.Thread(target=self.recv_message)
        t2.start()
        self.textbox.returnPressed.connect(self.send_message) #if they press enter, then call send_message fn        
#        self.isclosed = False #doesnt work

    def be_client(self):
        host = '127.0.0.1'
        port = 5000
        self.s = socket.socket()
        print "client socket opened"
        self.i = t(self.i,True)
        self.s.connect((host, port))
        self.label.setText("<connected>") 

    def be_server(self):
        host = '127.0.0.1'
        port = 5000
        self.ss = socket.socket()
        print "temp sock open"
        self.i = t(self.i,True)
        self.ss.bind((host,port))
        self.ss.listen(1)
        self.label.setText("<waiting to be connected>") 
        self.s, self.address = self.ss.accept()  #address is  ip address of what tries to connect
        self.ss.close()    
        print "temp client socket closed"
        self.i = t(self.i,False)
        self.label.setText("<connected>") 

    def send_message(self):
        message= self.textbox.text()
        if message != "":
            self.chathistory.append("Sent: " + str(message))
            self.s.send(message)
            self.textbox.clear()
        else:
            t2 = threading.Thread(target=self.recv_message)
            t2.start()
        sys.stdout.flush()
        
    def loner(self):
        self.label.setText("<Connection Lost>") 
        print "socket closed"
        self.s.close()
        self.i = t(self.i, False)
        print "^should be zero"
        self.textbox.setReadOnly(True)
        self.be_server()
        self.textbox.setReadOnly(False)
        t2 = threading.Thread(target=self.recv_message)
        t2.start()
        
    def recv_message(self):
#        try: #so it doesn't keep saying socket.timeout on console
        if 1 == 1:
            data= self.s.recv(1024)
#            print self.isclosed
#            if self.isclosed is True: #gonna send a blank message when u close window
#                self.label.setText("<connection closed>") 
#                print "got here"
            if data == "<close command>":
                print "Cmnd received"
                self.loner() 
#                self.label.setText("<Connection Lost>") 
#                print "socket closed"
#                self.i = t(self.i, False)
#                print "^should be zero"
#                self.s.close()
#                self.textbox.setReadOnly(True)
#                self.setup_networking()
            else:
                self.chathistory.append("Recieved: "+ str(data))
            sys.stdout.flush()
#        except socket.timeout: #we dont want it to keep saying it on the console
#            pass
#        except socket.error: #when it closes, need to make a new socket
#            self.s = socket.socket()
        
    def closeEvent(self,e):
        self.s.send("<close command>")
        print "cmd sent"
        print "closed window"        
        #self.isclosed=True
        print "socket closed"
        self.i = t(self.i, False)
        print "^ should be zero"
        self.s.close()
        
def t(x,add):
    if add:
        x = x + 1
    else:
        x = x - 1
    print x
    return x
        
def main():
    app = QApplication([])
    q = MyWidget()
    q.show()
    app.exec_()
    
if __name__ == "__main__":
    main()