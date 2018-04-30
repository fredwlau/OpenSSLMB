#!/usr/bin/python
# Import socket module
import socket
 
 
def Main():
    # local host IP '127.0.0.1'
    host = raw_input("Please enter the hostname of the server you would like to connect to:\n")
    addr = socket.gethostbyname(host)
    
    # Define the port on which you want to connect
    port = 1234
    
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    # connect to server on local computer
    s.connect((addr,port))
    
    #verify SSL
    data = s.recv(1024)
    ans = raw_input(data)
    a = ans.lower()
    s.send(a)
    if a == 'yes':
        data = s.recv(1024)
        print(data)
        data = s.recv(2048)
        print(data)
    
    #log in
    while True:
        
        data = s.recv(1024)
        if data == 'You are logged in\n':
            print(data)
            break
        if data == 'You are now registered and logged in\n':
            print(data)
            break
        if data == "You must register before logging in\n":
            continue
        else:
            ans = raw_input(data)
            s.send(ans)
    
    # messages
    data = s.recv(1024)
    print(data)
    while True:
        
        data = s.recv(1024)
        message = raw_input(data)
        s.send(message)
        if message == "END":
            break

        elif message == "GET":
            message = raw_input("Please enter a group name:\n")
            s.send(message)
            data = s.recv(1024)
            print(data)

        elif message == "POST":
            print("\n")
            message = raw_input("Please enter a group name:\n")
            s.send(message)
            message = raw_input("PLease enter a message you would like to post:\n")
            s.send(message)
            data = s.recv(1024)
            print(data)

        else:
            print("we should not get here\n")

    s.close()
 
if __name__ == '__main__':
    Main()
