# Author: Sphiwe Nyoni NYNSPH001
# Date (Last modified): 06/03/2023
# Program that connects to a remote server and exchanges files.


import hashlib
import os
import socket
import sys

buffer_size = 4096
separator = "<SEPARATOR>"


def get_hex(filename):  # calculates the hashlib of the file
    hasher = hashlib.md5()
    openfile = open(filename, "rb")
    content = openfile.read()
    hasher.update(content)
    return hasher.hexdigest()


def check_sum(server_file, client_file):  # compares the hashlib of two files
    if server_file == client_file:
        return True
    else:
        return False


def upload_file(s, filename, file_size):  # uploads the file to the server
    print("Uploading file...")
    file = open(filename, "rb")
    line = file.read(buffer_size)
    bytes_uploaded = 0
    rate = 0
    while line:
        s.sendall(line)
        current_rate = (bytes_uploaded / (file_size + 1)) * 100  # shows the rate at which the file is being uploaded
        if int(current_rate) >= rate:
            print(f"Uploading: {round(current_rate, 2)}%")
            rate += 10
        else:
            bytes_uploaded += buffer_size
        s.recv(buffer_size).decode()
        line = file.read(buffer_size)
    print("Uploading: 100%")
    s.sendall(b"DONE!")
    file.close()


def check_download(s, filename):  # checks whether the requested file can be downloaded from the server
    line = s.recv(buffer_size)
    if line == b"Failed!":
        print("File \"" + filename + "\" was not found!")
        return 0
    else:
        info = line.decode()
        info = info.split(separator)
        protected = info[0]
        file_size = int(info[1])
        if protected == "Y":
            key = input("The file is protected. Please enter pin:\n")
            s.send(key.encode())
        elif protected == "N":
            s.send("0000".encode())
        permission = s.recv(buffer_size).decode()
        if permission == "DENIED":
            print("Incorrect key. Request failed!")
            return 0
        else:
            print("Accepted")

        return download_file(filename, file_size, s)


def download_file(filename, file_size, s):  # download a file from the server
    file = open(filename, "wb")
    print("Downloading file...")
    bytesSent = 0
    rate = 0
    s.send("Receiving..".encode())
    line = s.recv(buffer_size)
    while (line != b"DONE!"):
        bytes_uploaded = (bytesSent / (file_size + 1)) * 100
        if int(bytes_uploaded) >= rate:
            print("Downloading:", round(bytes_uploaded, 2), "%")
            rate += 10
        file.write(line)
        s.send("Receiving..".encode())
        line = s.recv(buffer_size)
        bytesSent += buffer_size
    print("Downloading: 100%")
    file.close()
    return 1


def main():
    num_argv = len(sys.argv)
    if num_argv <= 3:  # uses default host and port number if user didn't specify
        host = socket.gethostname()
        port = 120
        query = input(
            "Enter command (U = Upload, V = View, D = Download, I = File info, R = Remove file, C = Close, E = Exist):\n").upper()

    elif num_argv > 3:  # assigns host and port as specified by th user
        host = sys.argv[1]
        port = sys.argv[2]
        query = ((sys.argv[3]).upper())[0:1]

    username = input("Enter your username: \n")
    password = input("Enter your password:\n")

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, int(port)))
            if query == "E":
                break
            elif query == "U":
                filename = input("Enter the name of the file:\n")
                file_basename = os.path.basename(filename)
                file_path = os.path.exists(filename)  # checks whether the file exists in the client
                while not file_path:
                    print(f"{filename} does not exist!!!")
                    filename = input("Enter the name of the file:\n")
                    file_path = os.path.exists(filename)
                file_size = os.path.getsize(filename)
                sum_file = get_hex(filename)
                protected = input("Is the file protected (Y/N):\n").upper()
                if protected == 'Y':
                    pin = input("Enter the access key (length of 5):\n")
                    while len(pin) < 5:
                        pin = input("Enter the access key (length of 5):\n")
                else:
                    pin = "0000"
                visibility = input("Is the file public (Y/N):\n").upper()

                s.sendall(query.encode())  # send query to upload to server
                print(f"From server: {s.recv(buffer_size).decode()}")

                s.sendall(file_basename.encode())
                print(f"From server: {s.recv(buffer_size).decode()}")

                upload_file(s, filename, file_size)  # uploads file to server
                file_info = visibility + separator + protected + separator + pin + separator + sum_file + separator + str(
                    file_size) + separator + username + separator + password + separator + "default"
                s.sendall(file_info.encode())
                print(f"From server: {s.recv(buffer_size).decode()}")

            elif query == "D":  # download
                s.sendall(query.encode())
                print(f"From server: {s.recv(buffer_size).decode()}")
                filename = input("Enter the name of the file to download:\n")
                file_base = os.path.basename(filename)
                s.send(file_base.encode())
                result = check_download(s, filename)
                if result == 0:
                    pass
                else:
                    s.send("SendInfo".encode())
                    server_file = s.recv(buffer_size).decode()
                    client_file = get_hex(filename)
                    if check_sum(server_file, client_file):
                        print("File is correct.")
                    else:
                        print("The file was corrupted in transit.")

            elif query == "V":  # view
                s.send(query.encode())
                print("Receiving the file list...")
                line = s.recv(buffer_size).decode()
                print(line)
                count = 1
                while line != "DONE!":
                    s.send("Receiving..".encode())
                    print(count, ".", line)
                    line = s.recv(buffer_size).decode()
                    count += 1
                print("View list processed")

            elif query == "I":  # get file info
                s.send(query.encode())
                prompt = s.recv(buffer_size).decode()
                filename = input("Enter the name of the File:\n")
                file_basename = os.path.basename(filename)
                s.send(file_basename.encode())
                print(s.recv(buffer_size).decode())

            elif query == "R":  # delete files from the server
                filename = input("Enter the name of the file to remove:\n")
                file_basename = os.path.basename(filename)
                line = file_basename + separator + username + separator + password
                s.send(query.encode())
                ack = s.recv(buffer_size).decode()
                s.send(line.encode())
                print(s.recv(buffer_size).decode())

            elif query == "C":  # close the connection
                s.send(query.encode())
                print(f"From Server: {s.recv(buffer_size).decode()}")
                break

            else:  # invalid request
                print("INVALID REQUEST")

            s.close()
            query = input(
                "Enter command (U = Upload, V = View, D = Download, I = File info, R = Remove file, C = Close, E = Exit):\n").upper()


if __name__ == "__main__":
    main()
