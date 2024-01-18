import RPi.GPIO as GPIO
from time import sleep


def water_mock(t, pin=None):
    sleep(t)

def water_pwm(t, pin=17, duty=50, frequency=500):
    '''
    t: seconds
    pin=14: pin number
    duty=40: duty cycle
    frequency=500: frequency
    '''
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        pwm = GPIO.PWM(pin, frequency)
        pwm.start(0)
        pwm.ChangeDutyCycle(100)
        sleep(0.2)

        for d in range(100, 0, -1):
            pwm.ChangeDutyCycle(d)
            sleep(0.01)
            if d == duty:
                sleep(t)
                break
        pwm.ChangeDutyCycle(0)
        GPIO.cleanup()

    except Exception as e:
        print(f'Exception: {e}')
        GPIO.cleanup()
    except BaseException as be:
        print(f'BaseException: {be}')
        GPIO.cleanup()

def water_one(t, pin=17):
    '''
    water with continuously high GPIO output
    '''
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 1)
        sleep(t)
        GPIO.output(pin, 0)
        GPIO.cleanup()
    except Exception as e:
        print(f'Exception: {e}')
        GPIO.cleanup()
    except BaseException as be:
        print(f'BaseException: {be}')
        GPIO.cleanup()
