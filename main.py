
# main.py

import sys
import os
import pickle

from network import * 
from readxml import * 
#from time import sleep

# the usage string to print when used improperly
USAGE = "SongSync\nTransfers over songs missing on the\
 client from the server!\n Usage: [--client (-c) | --server (-s)]\n"

MAX_THREADS = 8


def client():

	sock = create_socket()
	#init_connection(sock, socket.gethostbyname(socket.gethostname()))
	init_connection(sock, '127.0.0.1')
	#print "Connected to", socket.gethostbyname(socket.gethostname())
	
	# get string representation of song dict
	xmlfile = open_file(TEST_CLI_FILE)	
	songs = get_songs(xmlfile)
	close_file(xmlfile)	
	print "Read in client songs"
	
	#song_list_bytes = sys.getsizeof(song_data)
	message = create_message(SONG_LIST, songs)
	
	sock.send(message)
	print "Sent client song list"
	
	#missing_dat = pickle.loads( recv_data(sock) )
	dat_type, dat_len = recv_msg_header(sock)
	if SONG_NUM in dat_type:
		num_missing = pickle.loads(recv_data_chunk(sock, dat_len))
		#num_missing = missing_dat[1]
	
	print "Missing", num_missing, "songs"
	
	# create some threads to make connections and get songs
	
	close_socket(sock)

	return
	
	
def server():

	listen_sock = create_socket()
	
	bind_addr(listen_sock)
	data_sock, cli_addr = wait_for_connection(listen_sock)
	print cli_addr, "connected"
		
	# recv client song list
	dat_type, dat_len = recv_msg_header(data_sock)
	if SONG_LIST in dat_type:
		#dat = recv_data_chunk(data_sock, dat_len)
		#print dat
		#cli_songs = pickle.loads(dat)
		cli_songs = pickle.loads(recv_data_chunk(data_sock, dat_len))
	else:
		print "expecting a song list!"
		exit(1)
	print "Recieved client song list"
	
	# read in my songs
	xmlfile = open_file(TEST_SERV_FILE)
	serv_songs = get_songs(xmlfile)
	close_file(xmlfile)
	print "Read in server songs"
	
	missing_songs = compute_missing_songs(serv_songs, cli_songs)
	print "Computed missing songs"

	#missing_dat = pickle.dumps( (SONG_NUM, unicode(len(missing_songs))) )
	missing_dat = create_message(SONG_NUM, len(missing_songs))
	#print missing_dat
	data_sock.send( missing_dat )
	print "Sent missing song data"
		
	# create threads to send songs
	
	# send songs
	
	#os.path.getsize("/path/isa_005.mp3")
	
	close_socket(listen_sock)
	close_socket(data_sock)

	return



def main():

	if (len(sys.argv) > 1):
		if(sys.argv[1] == '--client' or sys.argv[1] == '-c'):
			client()
		elif(sys.argv[1] == '--server' or sys.argv[1] == '-s'):
			server()
		else:
			print USAGE
	else:
		print USAGE
	
	return



if __name__ == "__main__":
    main()