import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


class ThirdActivity():

	def __init__(self, *args):

		self.spi = busio.SPI(clock = board.SCK, MISO = board.MISO, MOSI = board.MOSI)
		self.cs  = digitalio.DigitalInOut(board.CE0)
		self.mcp = MCP.MCP3008(self.spi, self.cs)
		self.ch  = AnalogIn(self.mcp, MCP.P0)

	def read_ch (self):
		return self.ch.value
