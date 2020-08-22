import digitalio
import board
from flask import Flask, jsonify, abort, request
from flask_restful import Resource, Api
from threading import Thread
# import sys, os

_quit = False

class FourthActivity():
	def __init__(self,*args):
		#led and button objects
		self.led = digitalio.DigitalInOut(board.D4)
		self.led.direction = digitalio.Direction.OUTPUT

	def led_on(self):
		self.led.value = False
		return True

	def led_off(self):
		self.led.value = True
		return False

class gpio_pin(Resource):

	def get(self, id):
		if len(id) == 0:
			abort(404)

		return jsonify({" gpio": id})

class gpiod4(Resource):

	def __init__(self):
		self.D4 = FourthActivity()

	def get (self, status):
		if status == "True":
			self.D4.led_on()
			return jsonify({" LED Is State": status})
		elif status == "False":
			self.D4.led_off()
			return jsonify({" LED Is State": status})
		else:
			return jsonify({" Send True or False"})


class api_status(Resource):

	def get(self):
		data = {
					'api_name' 	: 'JetsonRestApi',
					'version'  	: '0.1',
					'status'	: 'Success',
					'response'	: 'ping'
		}
		return jsonify(data)

class quit(Resource):

	def get(self, status):
		if status == "on":
			data = { "Still running"}
		elif (status == "off"):
			data = { "Shutting down"}
			_quit = True
		else:
			data = { "Send on or off"}

		return data

class JetsonRestApi(object):

	def __init__(self, name = "__main__", debug = False):

		self.app = Flask (name)
		self.api = Api(self.app)
		self.api.add_resource(gpio_pin, '/api/v0.1/gpio/<string:id>')
		self.api.add_resource(api_status, '/api/v0.1/api_status')
		self.api.add_resource(quit, '/api/v0.1/quit/<string:status>')
		self.api.add_resource(gpiod4, '/api/v0.1/gpiod4/<string:status>')
		self.server = Thread(name = name, target = self.start_server, \
		 args=(debug,), daemon = False)
		self.server.start()

	def start_server(self, mode = False):
		print ('[Flask  ] Starting Flask Server ...')
		self.app.run(host = "rb-desktop.local", port = 5000, debug = mode)

	def stop_server(self):
		print ('[Flask  ] Exiting Flask Server view ...')
		func = request.environ.get('werkzeug.server.shutdown')
		func()
		self.server.join()
		if not self.server.isAlive():
		 	print ('[Flask  ] Flask Server Closed...')

def main():
	serverFlask = JetsonRestApi("Embedded Systems")

	while _quit is not True:
		pass

	serverFlask.stop_server()
	#os.kill()

if __name__ == '__main__':
	main()



