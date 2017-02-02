import Adafruit_GPIO as GPIO
import Adafruit_GPIO.PWM as PWM

gpio = GPIO.get_platform_gpio()
pwm = PWM.get_platform_pwm()

class GenericValve:

    def open(self):
        pass

    def close(self):
        pass


class BallValve(GenericValve):

    def __init__(self, pin):
        self.pin = pin
        gpio.setup(self.pin, GPIO.OUT)

    def open(self):
        gpio.output(self.pin, GPIO.HIGH)

    def close(self):
        gpio.output(self.pin, GPIO.LOW)


class ServoValve(GenericValve):

    def __init__(self, pin):
        self.pin = pin

    def open(self):
        pwm.start(self.pin, 15, 100)
        pwm.stop(self.pin)

    def close(self):
        pwm.start(self.pin, 10, 100)
        pwm.stop(self.pin)


class Ignition:

    def __init__(self, pin):
        self.pin = pin
        gpio.setup(self.pin, GPIO.OUT)

    def start(self, p, m, s):
        if p and m and s:
            gpio.output(self.pin, GPIO.HIGH)

    def stop(self):
        gpio.output(self.pin, GPIO.LOW)