import RPi.GPIO as GPIO
import time

def distance(a,b):
    GPIO.output(a, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(a, GPIO.LOW)
    while not GPIO.input(b):
        pass
    t1 = time.time()
    while GPIO.input(b):
        pass
    t2 = time.time()
    
    return (t2-t1)*340/2


def ledStatus(a,b):
    if a < 0.04:
        lcd.lcd_string("WET BIN FULL",LCD_LINE_1)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(15, GPIO.LOW)
    elif a > 0.06 and a <0.10:
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(15, GPIO.LOW)
    elif a>0.10:
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(15, GPIO.LOW)
    
    if b < 0.04:
        lcd.lcd_string("DRY BIN FULL",LCD_LINE_2)
        GPIO.output(19, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
    elif b > 0.06 and b <0.10:
        GPIO.output(19, GPIO.HIGH)
        GPIO.output(21, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
    elif b>0.10:
        GPIO.output(19, GPIO.HIGH)
        GPIO.output(21, GPIO.HIGH)
        GPIO.output(12, GPIO.LOW)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#ultrasonic sensor pin assignment
GPIO.setup(16,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(18,GPIO.IN)
GPIO.setup(24,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(26,GPIO.IN)


time.sleep(2)

try:
    while True:
        a = round(distance(16,18),2)
        b = round(distance(24,26),2)
        ledStatus(a,b)
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()