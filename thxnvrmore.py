#!/usr/bin/env python3
import os 
import pyaudio
import wave
import random
from time import sleep
import RPi.GPIO as GPIO
#import aiy.audio
import aiy.cloudspeech
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

        self.recog = aiy.cloudspeech.get_recognizer()
        # expect pause command
        self.recog.expect_phrase('pause')
        # expect shuffle command
        self.recog.expect_phrase('shuffle')
        # expect next command
        self.recog.expect_phrase('next')

        # expect volume commands
        for i in range(0, 101):
            self.recog.expect_phrase('volume {} percent'.format(i))


        self.songs_dir = get_song_dir()
        self.songs = get_songs(self.songs_dir)
        self.paused = True 

    def shuffle_songs(self):
        ''' Shuffles the song order '''
        random.shuffle(self.songs)

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
                # debounce
                sleep(0.2)
                print('\n[BUTTON PRESSED] - Music paused')

                voice_cmd = self.recog.recognize()

                if voice_cmd == 'pause':
                    while GPIO.input(self.button_pin) == True:
                        pass

                elif voice_cmd == 'next':
                    sleep(0.2)
                    return

                elif voice_cmd.startswith('volume'):
                    print('[VOLUME CHANGE]')

                elif voice_cmd == 'shuffle':
                    self.shuffle_songs()
                    sleep(0.2)
                    return

                else:
                    print('[VOICE COMMAND NOT RECOGNIZED] - {}'.format(voice_cmd))


                # debounce
                sleep(0.2)

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
