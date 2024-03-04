# Client-server
A python-based client-server file-server application for uploading/downloading files to/from the server. Connection is rendered using TCP. 

# Server Implementation
The server is implemented to only accept messages of a certain size from a client at a time. This is the variable
buffer size which sets a limit of 4096 bytes. Each file uploaded to the server is stored in a dictionary defined
as dictFiles where the filename is used as a key for information on the file. Each file is accompanied by
relatively relevant information such as password if the file is protected, visibility (whether the file is visible
to everyone or not), file size, etc. The server implements a variety of methods designed to fulfill user
requirements such as uploading and downloading a file

# Client Implementation
In this client class, the client is permitted to upload and download files to and from the server. They are also
allowed to view only publicly visible available files, delete files only if that specific client uploaded the file,
request information on a particular file, close the socket connection, and exist. Before the client can
perform these actions, the client must log into the server using a username and password, which is used to identify
the client. If the client wishes to upload a file to the server, they are required to specify whether the file is
protected and if the file is publicly visible or hidden. Given that the client wishes to protect the file the client
is required to specify the password that can be used to download the file – only clients with this encryption
key are allowed to download the file. Given the file being uploaded is not protected, a default password “0000”
which won’t be required when downloading the file from the server is given to that file and this is done to
ensure consistency in keeping information about the file. The information related to a file is made up of
visibility status, whether it’s protected, encryption key, hash value of the file, file size, username, and
client password. This username and password are important when the client wishes to delete a file from the
server since only the client who uploaded the file can delete it from the server, so both the username and
password are used to identify the individual client. The client can view files currently on the server that are
available for the public to view. This client, however, cannot view files that are hidden. Hidden files cannot
be viewed by any client even though that particular client is the one who uploaded the file. The rationale
behind this is security. A different client, client X, may get hold of client Y's username and password but this
should not allow client X to view every file belonging to client Y. This feature thus provides an extra layer of
security. The client implements methods similar to the server and these methods allow the client to perform
actions essential to fulfilling requirements and these methods include download_file which allows the user to
download a file from the server and check_sum which allows the client to compare the hash value for it’s file
and the hash value for the server’s file thus conserving the integrity of the transmitted file. The client can
perform multiple actions in one implementation.

# Stress test
The system does not implement any multithreading meaning our system can perform one query at a time 
before performing another query for another client 2. client 1’s connection must be closed to be able to
establish a connection with client 2. This means that a client must wait for the first client to finish before they
could be able to perform their query. Since simultaneous access is not available a client disconnects after
running their query and gives space for the client in waiting to connect. The protocol supports uploading files
of different types and file sizes with the use of a buffer size of 4 kilobytes (4096 bytes) per time and transmits
the files in seconds or a few minutes.

# To improve
1. Allow multiple users to connect to the server concurrently (multithreading and concurrency).
2. Add user interface

# Diagrams
![Download_Process_Sequence_Diagram](https://github.com/snmyk/Client-server/assets/67907125/310e08b1-7165-4c1c-a19b-18f41722b629)
![Screenshot (281)](https://github.com/snmyk/Client-server/assets/67907125/e8b83dd8-9e5b-439f-9311-1f5d8bdd5c41)

