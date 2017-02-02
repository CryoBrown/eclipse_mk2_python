import Adafruit_GPIO as GPIO

gpio = GPIO.get_platform_gpio()

gpio.setup(26, GPIO.OUT)
gpio.output(26, GPIO.HIGH)

while(True):
	pass
