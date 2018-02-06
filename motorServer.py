from flask import Flask
from flask import request
import RPi.GPIO as GPIO
from time import sleep
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

app = Flask(__name__)

#move cart forward for PAUSE seconds
def forward():
        print("left forward")
        GPIO.output(Motor1A,GPIO.HIGH)  #left motor forward
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)

        GPIO.output(Motor2A,GPIO.HIGH)   #right motor forward
        GPIO.output(Motor2B,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.HIGH)

        sleep(2)
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

        sleep(PAUSE)
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

        sleep(PAUSE)
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

        sleep(PAUSE)
        print("Stopping motor")
        GPIO.output(Motor1E,GPIO.LOW)   #left motor
        GPIO.output(Motor2E,GPIO.LOW)   #right motor

#reads commands from vect and sends to motor
def runMotors(commandsVec):
    for command in commandsVec:
            if command == 'up':
                    forward()
            if command == 'down':
                    backwards()
            if command == 'left':
                    left()
            if command == 'right':
                    right()

@app.route('/start/')
def start():
    print('start')
    return "Hello World!"

@app.route('/stop/')
def stop():
    print('stop')
    return "goodbye World!"

#parses url parameters into commands ands stores in vector
@app.route('/load-commands/<commands>')
def load(commands):
    commandsVec = commands.split('-')
    runMotors(commandsVec)
    return "hello"

@app.route('/running/')
def running():
    print('running')
    return "goodbye World!"

atexit.register(GPIO.cleanup)

# app.run()
