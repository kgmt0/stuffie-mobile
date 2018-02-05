from flask import Flask
from flask import request
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
 
Motor1A = 16
Motor1B = 18
Motor1E = 22

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

app = Flask(__name__)

def forward():
	print "forward"
	GPIO.output(Motor1A,GPIO.HIGH)
	GPIO.output(Motor1B,GPIO.LOW)
	GPIO.output(Motor1E,GPIO.HIGH)
	sleep(2)
	print "Stopping motor"
	GPIO.output(Motor1E,GPIO.LOW)

def backwards():
	print "backwards"
	GPIO.output(Motor1A,GPIO.LOW)
	GPIO.output(Motor1B,GPIO.HIGH)
	GPIO.output(Motor1E,GPIO.HIGH)
	sleep(2)
	print "Stopping motor"
	GPIO.output(Motor1E,GPIO.LOW)

def runMotors(commandsVec):
	for command in commandsVec:
		if command == 'up':
			forward()
		if command == 'down':
			backwards()

@app.route('/start/')
def start():
	print'start'
    return "Hello World!"

@app.route('/stop/')
def stop():
	print 'stop'
    return "goodbye World!"

@app.route('/load-command/<commands>')
def load(commands):
    commandsVec = commands.split('-')
    runMotors(commandsVec)
    return

@app.route('/running/')
def running():
	print 'running'
    return "goodbye World!"


app.run()
GPIO.cleanup()