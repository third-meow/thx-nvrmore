#!/usr/bin/env python3
import os 
import RPi.GPIO as GPIO
import aiy.audio
import aiy.cloudspeech
import aiy.voicehat

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def get_song_dir():
    # get path to script, split into dir names
    path = os.path.realpath(__file__).split('/')
    # replace last branch of path with songs dir
    path[-1] = 'songs'
    # return as string
    return '/'.join(path)

def get_songs(path):
    '''
        Returns a list of paths to songs within a specified directory
    '''
    songs = []
    for filename in os.listdir(path):
        # full path to file
        filepath = os.path.join(path, filename)
        # if file is song
        if filename.endswith('.wav') or filename.endswith('.mp3'):
            songs.append(filepath)
        # if a directory
        elif os.path.isdir(filename):
            # recurse
            songs += get_songs(filepath)

    return songs

class Player:
    def __init__(self):
        self.button_pin = 23
        GPIO.setup(self.button_pin, GPIO.IN)
        self.light = aiy.voicehat.get_led()

        self.songs_dir = get_song_dir()
        self.songs = get_songs(self.songs_dir)


def main():
    p = Player()

if __name__ == '__main__':
    main()
