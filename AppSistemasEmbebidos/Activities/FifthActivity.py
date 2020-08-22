import digitalio
import board
# import simpleaudio as sa

class FifthActivity(object):

	def __init__(self,*args):
		#led and button objects
		self.led = digitalio.DigitalInOut(board.D4)
		self.led.direction = digitalio.Direction.OUTPUT
		# self.sound_wrong = sa.WaveObject.from_wave_file('wrong.wav')
		# self.sound_success = sa.WaveObject.from_wave_file('success.wav')

	def LoggedIn(self):
		self.led.value = False
		# self.sound_success.play()

	def WrogLogIn(self):
		self.led.value = True
		# self.sound_wrong.play()