import RPi.GPIO as GPIO
import time


GPIO.setwarning(False)
GPIO.setmode(GPIO.BOARD)
ir_sensor = 38
GPIO.setup(ir_sensor, GPIO.IN)

try:
    while True:
        if GPIO.input(ir_sensor):
            print("object detected")
        else:
            print("No object")
            
except KeyboardInterrupt:
    GPIO.cleanup()