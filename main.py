# -*- coding: utf-8 -*-

# main.py

import sys
import os
import pickle
import threading

from network import * 
from readxml import * 
#from time import sleep

# the usage string to print when used improperly
USAGE = "SongSync\nTransfers over songs missing on the\
 client from the server!\n Usage: [--client (-c) | --server (-s)]\n"
 
 

TEST_CLI_FILE = "test/cli.xml"
TEST_SERV_FILE = "test/serv.xml"
EMPTY_XML = "test/empty.xml"
XML_FILE = "/Users/stredger/Music/iTunes/iTunes Music Library.xml"
 
RECV_DIR = "new-songs/"

XML_CONSTS = {	'file://localhost':'',\
				'%20'	:	' ',\
				'%5D'	:	']',\
				'%5B'	:	'[',\
				'&#38;'	:	'&',\
				'%23'	:	'#',\
				'a%CC%88':	'ä',\
				'%C3%98':	'Ø',\
				'e%CC%81':	'é',\
				'a%CC%8A':	'å',\
				'u%CC%88':	'ü',\
				'o%CC%88':	'ö',\
				'%E2%80%A0':'†',\
				'%25'	:	'%',\
				'%C3%86':	'Æ',\
				'%C2%B0':	'°',\
				'%E2%82%AC':'€',\
				'e%CC%80':	'è',\
				'%3B'	:	';',\
				'%E2%99%A0':'♠',\
				'a%CC%80':	'à',\
				'n%CC%83':	'ñ'
			} 

MAX_THREADS = 8


def send_song(song, path, sock):

	for symbol, char in XML_CONSTS.iteritems():
	#	print "replacing", symbol, "with", char
		path = path.replace(symbol, char)
		
	print "Opening", path, "Size :", os.path.getsize(path)
	song_file = open_binary_file(path)
	song_bytes = song_file.read()
	close_file(song_file)
	
	#print "song length (bytes)", len(song_bytes)
	
	song_name = song + "." + path.split('.')[-1]
	song_dat = (song_name, len(song_bytes))
	
	song_msg = create_message(SONG_FILE, song_dat)
		
	sock.send(song_msg)
	sock.send(song_bytes)
	
	print "Sent song", song
	
	return
	
	
	
def recv_song(sock):

	msg_type, msg_len = recv_msg_header(sock)
	if SONG_FILE not in msg_type:
		print "Expecting song!"
		exit(1)
			
	song_head = pickle.loads(recv_data_chunk(sock, msg_len))
	song = song_head[0]
	song_len = song_head[1]
	print "receiving", song, "length:", song_len
	
	song_bytes = recv_data_size(sock, song_len)
	
	file = open(RECV_DIR + song, "w")
	file.write(song_bytes)
	close_file(file)
	
	print "wrote file", song
	
	return


def client():

	sock = create_socket()
	#init_connection(sock, socket.gethostbyname(socket.gethostname()))
	init_connection(sock, '127.0.0.1')
	#print "Connected to", socket.gethostbyname(socket.gethostname())
	
	# get string representation of song dict
	#xmlfile = open_file(TEST_CLI_FILE)
	xmlfile = open_file(EMPTY_XML)
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
	
	if not (os.path.isdir(RECV_DIR)):
		os.makedirs(RECV_DIR)

	# create some threads to make connections and get songs
	for i in range(num_missing):
		recv_song(sock)
	
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
	#xmlfile = open_file(TEST_SERV_FILE)
	xmlfile = open_file(XML_FILE)	
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
	for song in missing_songs:
		send_song(song, missing_songs[song], data_sock);
		
	
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