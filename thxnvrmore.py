#!/usr/bin/env python3
import os 
import pyaudio
import wave
import random
import subprocess
from time import sleep
import RPi.GPIO as GPIO
#import aiy.audio
import aiy.voicehat

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

CHUNK = 1024

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
    for filename in os.listdir(path): # full path to file
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

        self.c_vol = 25

        self.songs_dir = get_song_dir()
        self.songs = get_songs(self.songs_dir)
        self.paused = True 

    def shuffle_songs(self):
        ''' Shuffles the song order '''
        random.shuffle(self.songs)

    def cycle_volume(self):
        self.c_vol -= 5
        if self.c_vol == 0:
            self.c_vol = 25



        DEVNULL = open(os.devnull, 'w')
        subprocess.Popen(['amixer', 'sset', 'Master', '{}%'.format(self.c_vol)], stdout=DEVNULL)


    def play_wav(self, wav_path):
        ''' Plays wav file '''
        wf = wave.open(wav_path, 'rb')

        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(CHUNK)

        while data != '':
            stream.write(data)
            data = wf.readframes(CHUNK)
            if GPIO.input(self.button_pin) == False:
                count = 0
                while GPIO.input(self.button_pin) == False:
                    count += 1
                    sleep(0.001)

                if count >= 400 and count < 1200:
                    print('\n[BUTTON LONG PRESS] - Changing to next track')
                    return
                elif count >= 1200 and count < 3000:
                    print('\n[BUTTON VERY LONG PRESS] - Changing Volume')
                    self.cycle_volume()
                elif count >= 3000:
                    # shutdown code goes here
                    pass
                else:
                    print('\n[BUTTON SHORT PRESS] - Pausing music')
                    sleep(0.3) # debounce
                    while GPIO.input(self.button_pin):
                        pass

                sleep(0.2) # debounce

        stream.stop_stream()
        stream.close()

        p.terminate()

    def play(self):
        for song in self.songs:
            print('[PLAYING] {}'.format(song))
            self.play_wav(song)

        


def main():
    p = Player()
    p.shuffle_songs()
    p.play()

if __name__ == '__main__':
    main()
