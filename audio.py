"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time
import sys
import numpy as np
import struct

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

class player:

    # define callback (2)
    def callback(self, in_data, frame_count, time_info, status):

        data = self.wf.readframes(frame_count)

        # Unpack data, LRLRLR...
        y = np.array(struct.unpack("%dh" % (len(data) / self.SAMPLE_WIDTH), data))
        y_L = y[::2]
        y_R = y[1::2]

        Y_L = np.fft.fft(y_L, self.nFFT)
        Y_R = np.fft.fft(y_R, self.nFFT)

        # Sewing FFT of two channels together, DC part uses right channel's
        Y = abs(np.hstack((Y_L[-self.nFFT / 2:-1], Y_R[:self.nFFT / 2])))
        h = abs(hash(tuple(Y)))%16581375
        #print(abs(h)%16581375)
        R = h%255
        G = int((h/255)%255)
        B = int(h/(255*255))

        color_string = '#%02x%02x%02x' % (R, G, B);
        print(color_string)
        sys.stdout.flush()

        return (data, pyaudio.paContinue)

    def load_wav(self, wav):
        self.wf = wave.open(wav, 'rb')
        self.N_CHANNELS = self.wf.getnchannels()
        self.SAMPLE_WIDTH = self.wf.getsampwidth()
        self.RATE = self.wf.getframerate()
        self.nFFT = 512

    def play(self):
    # open stream using callback (3)
        self.stream = p.open(format=p.get_format_from_width(self.wf.getsampwidth()),
                    channels=self.wf.getnchannels(),
                    rate=self.wf.getframerate(),
                    output=True,
                    stream_callback=self.callback)


        # start the stream (4)
        while self.stream.is_active():
            time.sleep(0.1)

        self.stream.stop_stream()
        self.stream.close()
        self.wf.close()
        # close PyAudio (7)
        p.terminate()

ply = player()
ply.load_wav("music.wav")
ply.play()






