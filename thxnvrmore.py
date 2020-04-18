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
MAX_VOL = 20


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

    return sorted(songs)

class Player:
    def __init__(self):
        self.button_pin = 23
        GPIO.setup(self.button_pin, GPIO.IN)
        self.light = aiy.voicehat.get_led()

        self.c_vol = MAX_VOL

        self.songs_dir = get_song_dir()
        self.songs = get_songs(self.songs_dir)
        self.songs_orginal_order = self.songs
        self.shuffled = False
        self.paused = True 

    def shuffle_songs(self):
        ''' Shuffles the song order OR if already shuffled, unshuffles them '''
        if self.shuffled == False:
            random.shuffle(self.songs)
        else:
            self.songs = self.songs_orginal_order

    def cycle_volume(self):
        self.c_vol -= 5
        if self.c_vol == 0:
            self.c_vol = MAX_VOL

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

                if count > 500 and count < 2000:
                    print('\n[BUTTON LONG PRESS] - Changing Volume')
                    self.cycle_volume()
                elif count >= 2000:
                    print('\n[BUTTON VERY LONG PRESS] - Shuffle/Unshuffle')
                    self.shuffle_songs()
                    return 'SHUFFLE'
                else:
                    stream.stop_stream()
                    stream.close()
                    return 'PAUSE'

                sleep(0.2) # debounce

        stream.stop_stream()
        stream.close()
        return 'NEXT_TRACK'

        p.terminate()

    def play(self):
        for song in self.songs:
            print('[PLAYING] {}'.format(song))
            return_code = self.play_wav(song)
            if return_code == 'PAUSE':
                # wait for "play" signal
                while GPIO.input(self.button_pin) == True:
                    pass
            elif return_code == 'NEXT_TRACK':
                continue
            elif return_code == 'SHUFFLE':
                return



        


def main():
    p = Player()
    p.shuffle_songs()
    while True:
        p.play()

if __name__ == '__main__':
    main()
