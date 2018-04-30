#!/usr/bin/python

import hashlib
import os
import socket
from thread import*
from multiprocessing import Process
import threading
import ssl_generate

PATH = "messages"

print_lock = threading.Lock()

def threaded(c):
    message = "Would you like to verify this server's SSL certificate? Yes/No\n"
    c.send(message)
    answer = c.recv(100)
    a = answer.lower()
    if (a == "yes"):
        f = open('domain.crt', 'rb')
        l = f.read(2048)
        data = "Sending domain.crt...\n"
        c.send(data)
        c.send(l)
    data = "Have you logged into this server before? Yes/No\n"
    c.send(data)
    answer = c.recv(40)
    a = answer.lower()
    n = 0
    if a == "yes":
        n = login(c)
    else:
        n = register(c)
    if n != 0:
        while (n != 0):
            if os.path.isdir(PATH):
                groups = os.listdir(PATH)
                if groups == []:
                    data = "No groups available\n"
                else:
                    data = "The available groups are: "
                    for x in range(len( groups)):
                        data += groups[x]
                        data += " "
                    data += "\n"
            else:
                os.mkdir(PATH)
                data = "No groups available\n"
            c.send(data)
            while True:
                data = "Please send a command [GET|POST|END]\n"
                c.send(data)
                data = c.recv(1024)

                if data == "END":
                    data = "You have been disconnected from the server\n"
                    c.send(data)
                    c.close()

                elif data == "GET":
                    data = c.recv(1024)
                    group = PATH+"/"+data
                    if os.path.exists(group):
                        fh = open(group, "r")
                        buf = fh.read()
                        c.send(buf)
                        fh.close()
                    else:
                        data = "That group does not exist, please try again.\n"
                        c.send(data)

                elif data == "POST":
                    data = c.recv(1024)
                    group = PATH+"/"+data
                    data = c.recv(2048)
                    message = data+"\n"
                    fh = open(group, "a+")
                    fh.write(message)
                    data = "Message successfully posted.\n"
                    c.send(data)

                else:
                    data = "Invalid operation, please try again.\n"
                    c.send(data)
    
    else :
        data = "something about too many failed login attempts??"
        c.send(data)
    c.close()

def main():
    host = ""
    port = 1234
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    s.bind((host, port))
    print("Socket bound to port", port)

    s.listen(5)

    ssl_generate.create_self_signed_cert()

    while True:
        c, addr = s.accept()
        #print_lock.acquire()
        #thread.start_new_thread(threaded, (c, ))
        Process(target=threaded, args=(c,)).start()

    s.close()

def register(c):
    data = "Please input your desired username:\n"
    c.send(data)
    username = c.recv(100)
    data = "Please input your desired password:\n"
    c.send(data)
    password = c.recv(100)
    m = hashlib.md5()
    m.update(password)
    password = m.digest()
    file = open("accountfile.txt", "a")
    file.write(username)
    file.write(" ")
    file.write(password)
    file.write("\n")
    file.close()
    data = "You are now registered and logged in\n"
    c.send(data)
    return username

def login(c):
    data = "Please enter your username:\n"
    c.send(data)
    username = c.recv(100)
    found = 0
    for line in open("accountfile.txt", "r").readlines():
        login_info = line.split()
        if username == login_info[0]:
            found = 1
            break
        else:
          continue
    if found != 1:
        data = "You must register before logging in\n"
        c.send(data)
        register(c)
        return register(c)
    data = "Please enter your password:\n"
    c.send(data)
    password = c.recv(100)
    n = hashlib.md5()
    n.update(password)
    password = n.digest()
    didFind=0
    for line in open("accountfile.txt", "r").readlines():
        login_info = line.split()
        if username == login_info[0] and password == login_info[1]:
            data = "You are logged in\n"
            c.send(data)
            didFind=1
            return username
        else:
            continue
    count = 0
    while count < 3 and didFind == 0:
        data = "Wrong username or password, please try again"
        c.send(data)
        data = "Please enter your username:\n"
        c.send(data)
        username = c.recv(100)
        data = "Please enter your password:\n"
        c.send(data)
        password = c.recv(100)
        k = hashlib.md5()
        k.update(password)
        password = k.digest()
        file = open("accountfile.txt", "r")
        for line in file.readlines():
            login_info = line.split()
            if username == login_info[0] and password == login_info[1]:
                data = "You are logged in\n"
                c.send(data)
                didFind = 1
                return username
            else:
                continue
        count += 1
        file.close()
    data = "You have used all your login attempts\n"
    c.send(data)
if __name__ == "__main__":
    main()
