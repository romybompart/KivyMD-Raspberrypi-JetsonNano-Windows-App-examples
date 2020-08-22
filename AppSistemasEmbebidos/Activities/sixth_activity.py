from enum import Enum
from platform import system
import time

if system() == 'Linux':
	hardware = True
	import busio
	import digitalio
	import board
	from adafruit_bus_device.spi_device import SPIDevice
else:
	hardware = False



class SixthActivity():

	def __init__(self, *args):

		self.spi = busio.SPI(
				clock = board.SCK_1, 
				MISO = board.MISO_1, 
				MOSI = board.MOSI_1
				)
		self.cs  = digitalio.DigitalInOut(board.CE0_1)
		self._spi_device = SPIDevice(self.spi,self.cs)
		self._out_buf = bytearray(3)
		self._in_buf = bytearray(3)

	def spi_read_write(self, cmd):
		self._out_buf = [0x01, cmd, 0x02]
		self._in_buf = [0x00, 0x00, 0x00]
		with self._spi_device as spi:
			spi.write_readinto(self._out_buf, self._in_buf)
		return self._in_buf

	def spi_write(self,cmd):
		#self._out_buf = [0x01, cmd, 0x02]
		print( "Debut Tx -> {}".format(bytearray([cmd])))
		with self._spi_device as spi:
			spi.write(bytearray([cmd]))
		#return self._in_buf

	def spi_read(self):
		with self._spi_device as spi:
			byte = bytearray(1)
			spi.readinto(byte)
		return byte


class Commands(Enum):
	CMD_TURN_ON_RED 	= 0x05  #the command will start from 0x05    
	CMD_TURN_ON_BLUE 	= 0x06    
	CMD_TURN_ON_GREEN 	= 0x07   
	CMD_TURN_OFF_RED 	= 0x08    
	CMD_TURN_OFF_BLUE 	= 0x09   
	CMD_TURN_OFF_GREEN 	= 0x0A
	CMD_TURN_ALL_OFF	= 0x0B    
	CMD_TURN_ALL_ON 	= 0x0C     
	CMD_TURN_BG_ON 		= 0x0D      
	CMD_TURN_BR_ON 		= 0x0E     
	CMD_TURN_GR_ON 		= 0x0F
	CMD_ERROR			= 0xFF 

	def __init__(self, cmd):
		self.cmd = cmd
		self.hardware = hardware
		if self.hardware:
			self.hdw = SixthActivity()

	@property
	def send(self):
		if self.hardware:
			self.hdw.spi_write(self.cmd)
			# time.sleep(0.1)
			# return self.hdw.spi_read()
			#return self.hdw.spi_read(self.cmd)
		else:
			return [0x01,self.cmd,0x02]

#Test code
def main():
	psoc = SixthActivity()
	time.sleep(1)

	x = ''

	while (x !='s'):
		x = input()
		if(x == '1'):
			cmd = Commands.CMD_TURN_ON_RED.value
		elif(x == '2'):
			cmd = Commands.CMD_TURN_ON_BLUE.value
		elif(x == '3'):
			cmd = Commands.CMD_TURN_ON_GREEN.value
		elif(x == '4'):
			cmd = Commands.CMD_TURN_OFF_RED.value
		elif(x == '5'):
			cmd = Commands.CMD_TURN_OFF_BLUE.value
		elif(x == '6'):
			cmd = Commands.CMD_TURN_OFF_GREEN.value
		elif(x == '7'):
			cmd = Commands.CMD_TURN_ALL_OFF.value
		elif(x == '8'):
			cmd = Commands.CMD_TURN_ALL_ON.value
		elif(x == '9'):
			cmd = Commands.CMD_TURN_BG_ON.value
		elif(x == '10'):
			cmd = Commands.CMD_TURN_BR_ON.value
		elif(x == '11'):
			cmd = Commands.CMD_TURN_GR_ON.value
		else:
			cmd = Commands.CMD_ERROR.value

		psoc.spi_write(cmd)
		#print( "Debut Rx -> {}".format(a))
		# input()
		# a = psoc.spi_read()
		# print( "Debug Rx -> {}".format(a))

if __name__ == '__main__':
	main()
