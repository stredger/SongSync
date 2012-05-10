#readxml.py

import sys
import os

EXIT_FAIL = 1

TEST_CLI_FILE = "test/cli.xml"
TEST_SERV_FILE = "test/serv.xml"
XML_FILE = "/Users/stredger/Music/iTunes/iTunes Music Library.xml"

def open_file(path):
	
	#try:
	f_handle = open(path, 'r')
		
	#except IOError as (strerror):
	#	print "IOError: {1}".format(strerror)
	#	exit(EXIT_FAIL)

	return f_handle


# Pass in a file handle for closing
def close_file( file_h ):
	#try:
	file_h.close()
	#except AttributeError as (strerror):
	#	print "AttributeError: {0}".format(strerror)
	#	exit(EXIT_FAIL)
	
	return
	
	
# Traverses an iTunes library XML file getting songs and their
#	locations in the file system. If we find missing song names
#	or locations we print them to stdout.
# Returns a dictionary of (song name, network path) for
#	all the songs found in the XML file.
def get_songs(file):

	# holds (song, location) tuples
	songs = {}
	
	# holds songs with no location
	no_loc = []
	
	# holds locaions with no song
	no_song = []
			
	line = file.readline()
	while (line != ""):
	
		# find song names
		if ('>Name<' in line):
			song = line.split('<string>')[1].split('</string>')[0]
			line = file.readline()
			
			# we found a name so look for a location
			while ('</dict>' not in line) and (line != ""):
			
				# we found a playlist not a song
				if ('>Playlist ID<' in line):
					song = None
					break
			
				if ('>Location<' in line):
					# we found a location, place the (song, loc) tuple 
					#	in songs and set song / loc to None so we know
					loc = line.split('<string>')[1].split('</string>')[0]
					songs[song] = loc
					song = loc = None
					break
				line = file.readline()
				
			# we found no location for the song name!
			if song is not None:
				no_loc.append(song)
			
		# we found a location before a song name!
		elif ('>Location<' in line):
			no_song.append(line.split('<string>')[1].split('</string>')[0])
			
		line = file.readline()
		
	# print song names with missing locations
	if len(no_loc):
		print "We failed to find locations for:"
		for song in no_loc:
			print ">> " + song
	
	# print locations with missing song names
	if len(no_song):
		print "We failed to find song names for:"
		for loc in no_song:
			print ">> " + loc.strip()
	
	return songs


# Computes the songs that appear in serv_song but not cli_song
# Returns a (name, path) dictionary of the missing songs 
def compute_missing_songs(serv_songs, cli_songs):

	missing_songs = {}
	
	for song in serv_songs:
		if not (cli_songs.has_key(song)):
			missing_songs[song] = serv_songs[song]
	
	return missing_songs


"""
def main():

	#cli_xml = open_file(XML_FILE)

	cli_xml = open_file(TEST_CLI_FILE)
	serv_xml = open_file(TEST_SERV_FILE)
	
	cli_song_list = get_songs(cli_xml)
	serv_song_list = get_songs(serv_xml)
		
	missing_songs = compute_missing_songs(serv_song_list, cli_song_list)
	
		
	close_file(cli_xml)
	close_file(serv_xml)

	return


if __name__ == "__main__":
    main()
"""