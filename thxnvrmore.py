#!/usr/bin/env python3
import os 
import RPi.GPIO as GPIO
import aiy.audio
import aiy.cloudspeech
import aiy.voicehat

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Player:
    def __init__(self):
        self.button_pin = 23
        GPIO.setup(self.button_pin, GPIO.IN)
        self.light = aiy.voicehat.get_led()

        self.songs_dir = ''.join(['/' + x for x in os.path.realpath(__file__).split('/')[1:-1]]) + '/songs'
        print(self.songs_dir)

def main():
    p = Player()

if __name__ == '__main__':
    main()
