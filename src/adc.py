import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

def bytes_to_int(bytes):
	return int(codecs.encode(bytes, 'hex'), 16)

def bitstring_to_bytes(s):
	v = int(s, 2)
	b = bytearray()
	while v:
	    b.append(v & 0xff)
	    v >>= 8
	return bytes(b[::-1])

gpio = GPIO.get_platform_gpio()

CONFIGURATION_COMMAND = bitstring_to_bytes("1110000000011101")

class ADC(object):
	
	def__init__(self, sclk, mosi=None, miso=None, ss=None):
		self.bb = SPI.BitBang(gpio, sclk, mosi, miso, ss)
		self.bb.set_bit_order(SPI.MSBFIRST)
		self.bb.set_mode(2)
		self.bb.write(CONFIGURATION_COMMAND) //determine start conf
		self.read_length = 16

	def read(channel):
		if channel < 0 or channel > 7 :
			print("Hey you're fucking up")

		hex_str = str(channel) + "000"
		channel_command = bytearray.fromhex(hex_str)

		self.bb.write(channel_command)

		//Do we need to wait before we do this?
		data = self.bb.read(self.read_length)

		max = bytearray.fromhex("".join(["f"] * self.read_length))
		output = float(bytes_to_int(data)) / bytes_to_int(max) //get a percentage of maximum output we are receving

		return output



