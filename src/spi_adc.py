import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

gpio = GPIO.get_platform_gpio()

CONFIGURATION_COMMAND = [int("11100000", 2), int("00011111", 2)]

READ_COMMAND = [13 << 4, 0]

class ADC(object):
	
	def __init__(self, sclk, mosi=None, miso=None, ss=None):
		self.bb = SPI.BitBang(gpio, sclk, mosi, miso, ss)
		self.bb.set_bit_order(SPI.MSBFIRST)
		self.bb.set_mode(2)
		self.bb.transfer(CONFIGURATION_COMMAND) #determine start conf
		self.read_length = 2

	def read(self, channel):
		if channel < 0 or channel > 7 :
			print("Hey you're fucking up")

		channel_command =  [channel << 4, 0]
		print self.bb.transfer(channel_command)
		print self.bb.transfer(READ_COMMAND)
		print self.bb.read(self.read_length)
		
	def read_cfr():
		self.bb.write([12 << 4, 0])
		self.bb.write(READ_COMMAND)
		return self.bb.read(self.read_length)

