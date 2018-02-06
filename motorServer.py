#!/usr/bin/env python3
# vim: set sw=4 ts=4 et:

import RPi.GPIO as GPIO
from time import sleep
from threading import Thread
from threading import Event
from threading import Condition
from queue import Queue
import signal
import http.server
import atexit

PAUSE = 2   #number of seconds the motors will turn in any call to power motors

GPIO.setmode(GPIO.BOARD)

Motor1A = 16
Motor1B = 18
Motor1E = 22

Motor2A = 23
Motor2B = 21
Motor2E = 19

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

worker_cv = Condition()
motor_commands = Queue()
exit = False
stop = Event()

#move cart forward for PAUSE seconds
def forward():
        print("left forward")
        GPIO.output(Motor1A,GPIO.HIGH)  #left motor forward
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)

        GPIO.output(Motor2A,GPIO.HIGH)   #right motor forward
        GPIO.output(Motor2B,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.HIGH)

        stop.wait(2)
        print("Stopping motor")
        GPIO.output(Motor1E,GPIO.LOW)   #left motor
        GPIO.output(Motor2E,GPIO.LOW)   #right motor

#move cart back for PAUSE seconds
def backwards():
        print("backwards")
        GPIO.output(Motor1A,GPIO.LOW)   #left motor back
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor1E,GPIO.HIGH)

        GPIO.output(Motor2A,GPIO.LOW)   #right motor back
        GPIO.output(Motor2B,GPIO.HIGH)
        GPIO.output(Motor2E,GPIO.HIGH)

        stop.wait(PAUSE)
        print("Stopping motor")
        GPIO.output(Motor1E,GPIO.LOW)   #left motor
        GPIO.output(Motor2E,GPIO.LOW)   #right motor

#turns cart left by powering left motor back and right forward
def left():
        print("left")
        GPIO.output(Motor1A,GPIO.HIGH)  #left motor forward
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)

        GPIO.output(Motor2A,GPIO.LOW)   #right motor back
        GPIO.output(Motor2B,GPIO.HIGH)
        GPIO.output(Motor2E,GPIO.HIGH)

        stop.wait(PAUSE)
        print("Stopping motor")
        GPIO.output(Motor1E,GPIO.LOW)   #left motor
        GPIO.output(Motor2E,GPIO.LOW)   #right motor

#turns cart right by powering left motor forward and right back
def right():
        print("right")
        GPIO.output(Motor1A,GPIO.LOW)   #left motor back
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor1E,GPIO.HIGH)

        GPIO.output(Motor2A,GPIO.HIGH)  #right motor forward
        GPIO.output(Motor2B,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.HIGH)

        stop.wait(PAUSE)
        print("Stopping motor")
        GPIO.output(Motor1E,GPIO.LOW)   #left motor
        GPIO.output(Motor2E,GPIO.LOW)   #right motor

def process_motor_commands():
    commands_dict = {   "up":       forward,
                        "down":     backwards,
                        "left":     left,
                        "right":    right }
    with worker_cv:
        while not exit:
            if not motor_commands.empty():
                stop.clear()
                commands_dict[motor_commands.get()]()
            if motor_commands.empty():
                worker_cv.wait()

class StuffieMobileServer(http.server.SimpleHTTPRequestHandler):
    def load_commands(self, args):
        print(args)
        with worker_cv:
            print(args.split('-'))
            for i in args.split("-"):
                motor_commands.put(i)
            print(motor_commands.empty())
            worker_cv.notify()

    def stop(self):
        while not motor_commands.empty():
            motor_commands.get()
        stop.set()

    def do_GET(self):
        tokens = self.path.strip("/").split("/")
        print(tokens)

        if len(tokens) == 2 and tokens[0] == "load-commands":
            self.load_commands(tokens[1])
            self.send_response(200)
        elif len(tokens) == 1 and tokens[0] == "stop":
            self.stop()
            self.send_response(200)
        else:
            self.send_response(404)

        self.end_headers()

def shutdown(srv, worker):
    global exit
    exit = True
    with worker_cv:
        worker_cv.notify()
    worker.join()
    GPIO.cleanup()

def init():
    worker = Thread(target = process_motor_commands)
    worker.start()
    srv = http.server.HTTPServer(("0.0.0.0", 5000), StuffieMobileServer)
    cleanup = lambda *x: Thread(target = srv.shutdown).start()
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    srv.serve_forever()
    shutdown(srv, worker)

init()
