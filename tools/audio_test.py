#
# Audio test script
# Basically copied straight from pyaudio docs: http://people.csail.mit.edu/hubert/pyaudio/#docs
#

import pyaudio
import wave
import sys

CHUNK = 1024

def play_wav(wav_path):
    wf = wave.open(wav_path, 'rb')

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
            print('\nEnter any character to play or press Ctrl+C once more to quit')
            input()

    stream.stop_stream()
    stream.close()

    p.terminate()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
        sys.exit(-1)
    play_wav(sys.argv[1])
