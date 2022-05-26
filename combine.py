import RPi.GPIO as GPIO
import time
import lcd

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


def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(22, True)
    p.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(22, False)
    p.ChangeDutyCycle(0)


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

#led pin assignment
pins = [11,13,15,19,21,12]
for pin in pins:
        GPIO.setup(pin, GPIO.OUT)   # Set all pins' mode is output
        GPIO.output(pin, GPIO.HIGH)

#lcd setup
lcd.lcd_init()
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

#servo motor setup
servo=22
GPIO.setup(servo,GPIO.OUT)
p=GPIO.PWM(servo,50)# 50hz frequency
p.start(0)
SetAngle(90)

#moisture sensor setup
moisture = 40
GPIO.setup(moisture, GPIO.IN)

#IR Sensor setup
ir_sensor = 38
GPIO.setup(ir_sensor, GPIO.IN)


time.sleep(2)

try:
    while True:
        a = round(distance(16,18),2)
        b = round(distance(24,26),2)
        lcd.lcd_string("Waste Management",LCD_LINE_1)
        lcd.lcd_string("System",LCD_LINE_2)
        ledStatus(a,b)
        #SetAngle(90)
        #print(f"Sensor 1 dist = {a}m, Sensor 2 dist = {b}m")
        if GPIO.input(ir_sensor):
            print("No waste placed")
        else:
            time.sleep(4)
            if GPIO.input(moisture):
                lcd.lcd_string("Dry Waste",LCD_LINE_1)
                print ('No Water Detected!')
                SetAngle(45)
                time.sleep(4)
                SetAngle(90)
            else:
                print ('Water Detected!')
                lcd.lcd_string("Wet Waste",LCD_LINE_1)
                SetAngle(135)
                time.sleep(4)
                SetAngle(90)
        time.sleep(0.5)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
