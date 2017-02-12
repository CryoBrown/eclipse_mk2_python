from adc import ADC
adc = ADC(11, mosi=10, miso=9, ss=8)

for i in range(5):
	print adc.read(0)




import Adafruit_GPIO.SPI as SPI
#
# spi = SPI.SpiDev(0,0)
# spi.open()
# spi.set_clock_hz(5000)
# spi.set_mode(0)
# spi.set_bit_order(0)


