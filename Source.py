import socket
import pickle
import transfer_tools as tls
import time

# outline
# get a list of all DZT in the given directory
# Send the server a directory name
    # Server checks for the existance and contents of the provided directory
    # Server retiurns a list of the contained DZTs
# Do disjunctio of the two lists i.e. lists on the source not on the server, save as 
# 

# Constants
search_path = "C:\\Users\\Scott\\Desktop\\GPR_DATA\\Lincoln_Hill\\" 
#Host = '65.183.134.63'
Host = '127.0.0.1'
Port = 55

source_stack = tls.full_stack(search_path)

next_up = source_stack.pop()
dzt_obj = tls.DZT_DAT(next_up)
pickled_dzt = pickle.dumps(dzt_obj)
server_stack = ['empty']
print("Waiting for Connection to Host")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((Host, Port))
    print("Connected to ", Host)
    
    # Prompt the user for the name of the survery and send it off
    print("Sending Directory...")
    #directory =  "DIR " + input("Enter Survey Directory: ")
    directory = "DIR Lincoln_Hill"
    tls.gen_send(s,directory)
    response = tls.gen_recv(s)
    print("response: ",response)
    
    # Send the list of files on the source machine, need to recive the list of files on the server
    print("Sending Source Stack...")
    tls.gen_send(s,source_stack)
    response = tls.gen_recv(s)
    print("response: ",response)
    request_stack = tls.gen_recv(s)
    print("request stack: ",request_stack)
    
    print("Sending Files...")
    while request_stack != []:
        next_file = request_stack.pop()
        print("Sending ",next_file)
        next_dzt = tls.DZT_DAT(next_file)
        tls.gen_send(s,next_dzt)
        response = tls.gen_recv(s)
        print(response)
    print("Stack Empty")
    
    # Close the socket
    print("Closing Connection...")
    tls.gen_send(s,"COM exit")
    response = tls.gen_recv(s)
    print("response: ",response)
