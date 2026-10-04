import socket
from PIL import Image


my_sock = socket.socket()

#connect to server
try:
    my_sock.connect(("127.0.0.1",1450))
except Exception as e:
    my_sock.close()
    exit(f"server is down - try again {str(e)}")

while True:
    msg = input("enter one of the following commands: screenshot, copy, paste, software, data, delete, copyfile, exit. ")
    if msg.lower() == "exit":
        break

    try:


        my_sock.send(msg.encode())

        if msg.lower() == "screenshot":


            file_data_len = int(my_sock.recv(6).decode())

            data_recv = b''
            while len(data_recv) < file_data_len:
                slice = file_data_len - len(data_recv)
                if slice > 1024:
                    data_recv += my_sock.recv(1024)
                else:
                    data_recv += my_sock.recv(slice)



            #put the data of the image inside a file so it will open as an image
            with open(r'pic.jpg', 'wb') as file:
                file.write(data_recv)
            #open the image and continue

            im = Image.open("pic.jpg")
            im.show()
            continue

        elif msg.lower() == "copy":
            name = input("enter a message to copy to clipboard ")
            my_sock.send(str(len(name)).encode())
            my_sock.send(name.encode())
            print(my_sock.recv(1024).decode())
        elif msg.lower() == "paste":
            paste_data = my_sock.recv(1024).decode()
            print(paste_data)
        elif msg.lower() == "software":
            name = input("enter a software you want to open ")
            my_sock.send(str(len(name)).encode())
            my_sock.send(name.encode())
            open_data = my_sock.recv(1024).decode()
            print(open_data)
        elif msg.lower() == "data":
            name = input("enter file location on computer ")
            my_sock.send(str(len(name)).encode())
            my_sock.send(name.encode())
            file_info = my_sock.recv(1024).decode()
            print("the info of the folder is: ", file_info)
        elif msg.lower() == "delete":
            name = input("enter file path ")
            my_sock.send(str(len(name)).encode())
            my_sock.send(name.encode())
            file_del = my_sock.recv(1024)
            print(file_del)
        elif msg.lower() == "copyfile":
            file_to_copy = input("enter a file to copy ")
            dest_file = input("enter your destination file ")
            my_sock.send(str(len(file_to_copy)).encode())
            my_sock.send(file_to_copy.encode())
            my_sock.send(str(len(dest_file)).encode())
            my_sock.send(dest_file.encode())
            print(my_sock.recv(1024).decode())
    except Exception as e:
        print(f"error in receive or sending data {str(e)}")
        break
my_sock.close()
print("Bye Bye, have a great day!")