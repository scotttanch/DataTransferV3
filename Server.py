import pickle
import socket
import transfer_tools as tls
import time
import os

print("Waiting for Connection to Client")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    # Begin listening at the desired port
    #Host = "192.168.0.199"
    Host = '127.0.0.1'
    Port = 55
    s.bind((Host, Port))
    s.listen()
    project_directory = 'C:\\Users\Scott\\Desktop\\Surveys\\'
    # Accept connection to the source
    conn, addr = s.accept()
    print('Connected to', addr)
    with conn:
        while True:
            # Receive the etirety of an objects bin and unpickle i
            print("started reciving")
            recv_obj = tls.gen_recv(conn)
            tls.gen_send(conn,"ACK")

            # This should be what to do with a provided directory or command
            if type(recv_obj) == str:
                # Is the string a command or a directory?
                if recv_obj.startswith('COM'):
                    # Commands go here
                    command = recv_obj.split(' ')[-1]
                    if command == "exit":
                        print("Closing socket")
                        break
                if recv_obj.startswith('DIR'):
                    directory = recv_obj.split(' ')[-1]
                    if os.path.exists(project_directory+directory) == False:
                        os.mkdir(project_directory+directory)
                # rec_obj will either be a directory or a command to say were done
                # Check for the existance of the directory
            
            # This should be what to do with the source_stack
            if type(recv_obj) == list:
                source_list = recv_obj
                server_list = tls.full_stack(project_directory+directory)
                print("source list:")
                for file in source_list:
                    print(file)
                print("Server list:")
                for file in server_list:
                    print(file)
                requests = list(set(source_list)-set(server_list))
                print("Requests:")
                for file in requests:
                    print(file)
                tls.gen_send(conn,requests)
                #conn.sendall(b"you sent a list")
                # return files in source_list not in server_list

            # This should be what to do with a DZT obj
            if type(recv_obj) == tls.DZT_DAT:
                print("Got a DZT")
                # write the DZT and associated CSV
                print("Saving File")
                with open(recv_obj.file_name,'wb+') as f:
                    f.write(recv_obj.dzt_contents)
                if recv_obj.realsense_contents != []:
                    with open(recv_obj.realsensefile,'wb+') as f:
                        f.write(recv_obj.realsense_contents)
                print("Generating B Scan")
                recv_obj.b_scan()