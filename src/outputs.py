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
	pwm.start(self.pin, 13, 100)

    def open(self):
        pwm.set_duty_cycle(self.pin, 21)

    def close(self):
        pwm.set_duty_cycle(self.pin, 13)

class Enable:
    def __init__(self, pin):
        self.pin = pin
        gpio.setup(self.pin, GPIO.OUT)

    def enable(self):
        gpio.output(self.pin, GPIO.HIGH)

    def disable(self):
        gpio.output(self.pin, GPIO.LOW)


class Ignition:

    def __init__(self, pin):
        self.pin = pin
        gpio.setup(self.pin, GPIO.OUT)

    def start(self):
        gpio.output(self.pin, GPIO.HIGH)

    def stop(self):
        gpio.output(self.pin, GPIO.LOW)
