# network.py

import socket
import pickle

PORT = 44444
MAX_CON = 10
MAX_READ = 4096

SONG_LIST = "SLst"
SONG_FILE = "SFle"
SONG_NUM = "SNum"
FILE_LEN = "FLen"
MAX_FILE_SIZE = 999999999 # 1GB - 1B, do it in hex???
HEADER_LEN = len(SONG_LIST) + len(unicode(MAX_FILE_SIZE)) + 2 # +2 for the ;'s
HEADER_SEP = ";"


# creates a socket for TCP and make reusable
def create_socket():

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	
	return sock


# closes a socket
def close_socket(sock):
	sock.close()
	return
	
	modif
	
#
def make_header_string(num):	
	
	if (num > MAX_FILE_SIZE):
		print "File size to large to send"
		exit(1)
	
	str = unicode(num)
	while (len(str) < len(unicode(MAX_FILE_SIZE))):
		str = "0" + str
	
	return str
	
	
#
def create_message(msg_type, data):

	raw_data = pickle.dumps(data)
	msg_len = make_header_string(len(raw_data))
	msg = msg_type + HEADER_SEP + msg_len + HEADER_SEP + raw_data
	#print msg
	return msg


#
def recv_msg_header(sock):

	head = recv_data_chunk(sock, HEADER_LEN)
	msg_type = head.split(HEADER_SEP)[0]
	msg_len = int(head.split(HEADER_SEP)[1])
	
	return msg_type, msg_len


# binds the socket to internet interface and enables it to listen
def bind_addr(sock):
 
	#sock.bind( (socket.gethostbyname(socket.gethostname()), PORT) )
	sock.bind( ('127.0.0.1', PORT) )
	sock.listen(MAX_CON)
	return


# initiates a connection to the address addr
def init_connection(sock, addr):

	sock.connect((addr, PORT))
	return


# 
def wait_for_connection(sock):

	(cli_sock, cli_addr) = sock.accept()	

	return (cli_sock, cli_addr)
	

# Recieves all data sent to the socket
# Returns socket contents in a string obj
def recv_data(sock):

	data = ""
	try:	
		chunk = sock.recv(4096)
		sock.setblocking(0) # there must be a better way of doing this...
		while (chunk != ""):
			data += chunk
			chunk = sock.recv(4096)
			
		sock.setblocking(1)	# there must be a better way of doing this...
	except IOError:
		None
	return data


#
def recv_data_size(sock, num_bytes):

	data = ""
	to_read = num_bytes if num_bytes < MAX_READ else MAX_READ
	try:	
		data = sock.recv(to_read)
		num_bytes -= to_read

		while (num_bytes > 0):
			to_read = num_bytes if num_bytes < MAX_READ else MAX_READ
			chunk = sock.recv(to_read)
			if (chunk == ""):
				break
			data += chunk
			num_bytes -= to_read

	except IOError:
		None
		
	return data


#
def recv_data_chunk(sock, chunk_size):

	chunk = ""	
	try:
		chunk = sock.recv(chunk_size)
	except IOError:
		None
		
	return chunk


#select.select(potential_readers, potential_writers, potential_errs, timeout)
	
"""
def main():
	s = create_socket()
	
	
	#bind_addr(s)
	#wait_for_connection(s)
	
	init_connection(s, socket.gethostbyname(socket.gethostname()) )
	
	close_socket(s)
	
	return


if __name__ == "__main__":
    main()
"""