"""
I'M SO SORRY LICENSE V. 1.0
I REALIZE THAT MY CODEBASE IS SHIT, BUT IT WORKS OKAY?
IF YOU USE THIS SOFTWARE, YOU IMMEDEATLY FORFEIT YOUR RIGHT TO EXECUTE
ME FOR BRINGING THIS HORROR ONTO THE PLANET EARTH. ALSO, IF YOU SOMEHOW
GIVE THIS SOME SORT OF MIRACLE REFACTORING AND MAKES IT LESS DISGUSTING
WHILE STILL HAVING IT WORKING, PLEASE SHARE, BECAUSE THAT'D BE REALLY
COOL OF YOU. ALSO, THIS IS FREE SOFTWARE, AND COMES WITH NO WARRANTY
AND SUCH. IF YOU GET SUED BY SPOTIFY OR SOMETHING, YOUR DAMN FAULT.
DON'T BUG ME ABOUT IT. IDIOT.
"""

import dbus
import unicodedata
import urllib
import pyaudio
import wave
import os
import taglib
from dbus.mainloop.glib import DBusGMainLoop
import gobject
import sys
from optparse import OptionParser
from subprocess import Popen

from sys import byteorder
from array import array
from struct import pack

MusicDir = "home/julian/Music/"
addToPlaylist = False
skipRecorded = False

parser = OptionParser()
#We add it to the playlist of mpd
parser.add_option("-p", "--playlist", action="store_true", dest="playlistAdd", default=False)
#We skip already recorded songs
parser.add_option("-s", "--skiprecorded", action="store_true", dest="skipRecorded", default=False)

(options, args) = parser.parse_args()
addToPlaylist = options.playlistAdd
skipRecorded = options.skipRecorded


THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

#validFilenameChars = "-_.() %s%s" % (str.ascii_letters, str.digits)
def removeDisallowedFilenameChars(filename):
    return "".join([c for c in filename if c.isalpha() or c=='\'' or c.isnumeric() or c==" " or c=="(" or c==")" or c=="-" or c=="&"]).rstrip().encode('ascii', 'ignore')

dbus_loop = DBusGMainLoop(set_as_default=True)
def handler(arg1, arg2, arg3):
    if (isinstance(arg2, dict)):
        recmeta = arg2['Metadata']
        rawTitle = recmeta['xesam:title']
        fileTitle = removeDisallowedFilenameChars(recmeta['xesam:title'])
        rawArtist = recmeta['xesam:artist'][0]
        fileArtist = removeDisallowedFilenameChars(recmeta['xesam:artist'][0])
        rawAlbum = recmeta['xesam:album']
        fileAlbum = removeDisallowedFilenameChars(recmeta['xesam:album'])
        tracknumber = recmeta['xesam:trackNumber']
        albumDir = MusicDir + fileArtist + "/" + fileAlbum
        if "ad" not in recmeta['xesam:url']:
            if not os.path.exists(albumDir):
                os.makedirs(albumDir)
            fileURL = albumDir + "/" + fileTitle + ".wav"
            if not os.path.isfile(fileURL):
                record_to_file(fileURL, rawTitle, rawArtist, rawAlbum, tracknumber)
            else:
                if (skipRecorded):
                    print("Skipped already recorded song")
                    Popen("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next", shell=True)
            if not os.path.isfile(albumDir + "/cover.jpeg"):
                dl = recmeta['mpris:artUrl'].replace("open.spotify.com", "i.scdn.co")
                urllib.urlretrieve(dl, MusicDir + fileArtist + "/" + fileAlbum + "/cover.jpeg")
        else:
            #This script racks up a lot of memory leaks. This is how to deal with it.
            print("Restarting because an ad is playing")
            os.execl(sys.executable, *([sys.executable]+sys.argv))


session_bus = dbus.SessionBus(mainloop=dbus_loop)
spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify",
                                     "/org/mpris/MediaPlayer2")
spotify_properties = dbus.Interface(spotify_bus,
                                    "org.freedesktop.DBus.Properties")
spotify_interface = dbus.Interface(spotify_bus,
                                    "org.mpris.MediaPlayer2.Player")
metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")
session_bus.add_signal_receiver(handler)


def reconnect ():
    session_bus = dbus.SessionBus(mainloop=dbus_loop)
    spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify",
                                         "/org/mpris/MediaPlayer2")
    spotify_properties = dbus.Interface(spotify_bus,
                                        "org.freedesktop.DBus.Properties")
    spotify_interface = dbus.Interface(spotify_bus,
                                        "org.mpris.MediaPlayer2.Player")
    metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")

def getNewTitle ():
    spotify_properties = dbus.Interface(spotify_bus,
                                        "org.freedesktop.DBus.Properties")
    spotify_interface = dbus.Interface(spotify_bus,
                                        "org.mpris.MediaPlayer2.Player")
    metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")
    return metadata['xesam:title']

def record(title):
    """
    Record a word or words from the microphone and
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the
    start and end, and pads with 0.5 seconds of
    blank sound to make sure VLC et al can play
    it without getting chopped off.
    """
    reconnect()
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=2, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)
    song = title

    r = array('h')
    print("Recording " + title)
    while 1:
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        reconnect()
        if getNewTitle() != song:
            print(song + " recording complete!")
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    return sample_width, r

def record_to_file(path, title, artist, album, tracknumber):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record(title)
    data = pack('<' + ('h'*len(data)), *data)
    print("Stopped recording!")

    wf = wave.open(path, 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()
    f = taglib.File(path)
    f.tags["TITLE"] = [title]
    f.tags["ARTIST"] = [artist]
    f.tags["ALBUM"] = [album]
    f.tags["TRACKNUMBER"] = [str(tracknumber)]
    f.save()
    if addToPlaylist:
        #There have been issues with the database not having time to update, and therefore the song not being found. sleep 1 was the pragmatic solution to that.
        Popen('mpc update -h mpdpass@localhost --wait; sleep 1; mpc add -h mpdpass@localhost "' + path.replace(MusicDir, "") + '"', shell=True)
    else:
        Popen('mpc update -h mpdpass@localhost', shell=True)



reconnect()

loop = gobject.MainLoop()
loop.run()
