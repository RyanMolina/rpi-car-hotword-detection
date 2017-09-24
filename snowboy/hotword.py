import snowboydecoder
import sys
import signal
from car import Car
from motor import Motor
import RPi.GPIO as GPIO


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
car.speed = 50
car.start()
car.stop()


def hotWord(models):
    sensitivity = 0.5
    callbacks = [lambda: car.forward(),
                 lambda: car.turn_right(),
                 lambda: car.turn_left(),
                 lambda: car.reverse(),
                 lambda: car.stop()]
    detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
    print('Listening... Press Ctrl+C to exit')
    # main loop
    # make sure you have the same numbers of callbacks and models
    word = detector.start(sleep_time=0.03, detected_callback=callbacks)
    GPIO.cleanup()
    detector.terminate()

def main():
    words = ['pmdl/my_forward.pmdl', 'pmdl/my_right.pmdl', 'pmdl/my_left.pmdl',
             'pmdl/my_reverse.pmdl', 'pmdl/my_stop.pmdl']
    word = hotWord(words)


if __name__ == "__main__":
    main()

