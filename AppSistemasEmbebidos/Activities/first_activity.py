
import board
import digitalio
import operator


class FirstActivity():

	def __init__(self,*args):
		#led and button objects
		self.led = digitalio.DigitalInOut(board.D4)
		self.led.direction = digitalio.Direction.OUTPUT

		self.button1 = digitalio.DigitalInOut(board.D22)
		self.button1.direction = digitalio.Direction.INPUT

		self.button2 = digitalio.DigitalInOut(board.D18)
		self.button2.direction = digitalio.Direction.INPUT

	def xor_gate(self,*args):
		a, b  = self.operation(self.button1.value,'^',self.button2.value)
		return a, b

	def and_gate(self,*args):
		a, b  =  self.operation(self.button1.value,'&',self.button2.value)
		return a, b

	def or_gate(self,*args):
		a, b  =  self.operation(self.button1.value,'|',self.button2.value)
		return a, b

	def operation(self,a,b,c):
		ops = {
		'|': operator.or_ , 
		'&': operator.and_,
		'^': operator.xor
		}

		self.led.value = ops[b](a,c)

		if self.led.value:
			icon_text = "led-off"
		else:
			icon_text = "led-on"

		text = " Boton 1: {} | Boton 2: {} | Output: {} ".format(self.button1.value,self.button2.value,self.led.value)

		return text, icon_text
