#
# Audio test script
# Basically coped straight from pyaudio docs: http://people.csail.mit.edu/hubert/pyaudio/#docs
#

import pyaudio
import wave
import sys
from time import sleep

CHUNK = 1024

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(CHUNK)

while data != '':
    try:
        stream.write(data)
        data = wf.readframes(CHUNK)
    except KeyboardInterrupt:
        print('\nCtrl+C once more in next 3 seconds to quit')
        sleep(3)

stream.stop_stream()
stream.close()

p.terminate()
