from __future__ import print_function
from os import environ, path
from motor import Motor
from car import Car
from sphinxbase.sphinxbase import *
from pocketsphinx.pocketsphinx import *
import pyaudio
import RPi.GPIO as GPIO

def main():
    ena = 12
    enb = 16

    in1 = 7
    in2 = 11
    in3 = 13
    in4 = 15

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    right_wheel = Motor(ena, in1, in2)
    left_wheel = Motor(enb, in3, in4)

    car = Car(left_wheel, right_wheel)
    car.speed = 70
    car.start()

    MODELDIR = "/usr/local/share/pocketsphinx/model"
    CUSTOM_MODELDIR = "./"

    config = Decoder.default_config()
    config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
    config.set_string('-lm', path.join(CUSTOM_MODELDIR, '7215.lm'))
    config.set_string('-dict', path.join(CUSTOM_MODELDIR, '7215.dic'))

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
    stream.start_stream()

    try:
        print("Starting Decoder")
        decoder = Decoder(config)
        decoder.start_utt()
        while True:
            buf = stream.read(1024) 
            decoder.process_raw(buf, False, False)
            if decoder.hyp() != None:
                for seg in decoder.seg():
                    if seg.word == "FORWARD":
                        print("forward")
                        car.forward()
                    elif seg.word == "RIGHT":
                        print("right")
                        car.turn_right()
                    elif seg.word == "LEFT":
                        print("left")
                        car.turn_left()
                    elif seg.word == "REVERSE":
                        print("reverse")
                        car.reverse()
                    elif seg.word == "STOP":
                        print("stop")
                        car.stop()
                decoder.end_utt()
                decoder.start_utt()
    except:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
