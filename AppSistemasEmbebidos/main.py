"""
	Author: Romy Bompart
	Description: GUI created using kivy and kivymd (material design)
	date: 06/07/2020
"""
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.dialog import MDDialog
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineAvatarListItem
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox

from Activities.gauge_romy import Gauge
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from kivy.properties import BoundedNumericProperty
from kivymd.toast.kivytoast import toast
from kivy.utils import rgba
from kivymd.uix.button import MDFlatButton

from functools import partial
import requests
import json
import simpleaudio as sa
import time

import cv2
from Activities.camera_romy import KivyCamera
from kivy.uix.camera import Camera
#----------------------------------------------------------------------------------------------------------
Application = None
#----------------------------------------------------------------------------------------------------------
from platform import system
if system() == 'Linux':
	import os
	Hardware_data = True
	from Activities.first_activity import FirstActivity
	from Activities.third_activity import ThirdActivity
	from Activities.JetsonApiRest import FourthActivity
	from Activities.FifthActivity import FifthActivity
elif system() == 'Windows':
	Hardware_data = False
	import wmi
	w = wmi.WMI(namespace="root\wmi")

#----------------------------------------------------------------------------------------------------------

#Tabs Class
#https://kivymd.readthedocs.io/en/0.104.0/components/tabs/index.html?highlight=tabs#example-with-tab-icon
class Tab(FloatLayout, MDTabsBase):
	'''Class implementing content for a tab.'''
	pass

#AvatarItem Class
class AvatarItem(OneLineAvatarListItem):
    divider = None
    source = StringProperty()

#LeftIconItem Class
class LeftIconItem(OneLineAvatarListItem):
    icon = StringProperty()

#ListItemWithCheckBox
class ListItemWithCheckbox(OneLineAvatarIconListItem):
    '''Custom list item.'''
    icon = StringProperty("android")

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''
#------------------------------------------------------------------------------------------------------------

#opening page
class DashBoard(Screen):

	def on_enter(self):
		Clock.schedule_once(self.update_button_Text, 2)

	def update_button_Text(self, *args):
		#https://kivy.org/doc/stable/api-kivy.lang.html?highlight=root%20ids#ids
		self.ids["DashBtn"].text = "Get started"
		self.ids["DashBtn"].icon = "led-on"
		
#first screen activity
class FirstScreen(Screen):

	tabs_added = False
	event = None
	counter = [0,0,0]

	if Hardware_data:
		act1 = FirstActivity()

	def on_enter(self):
		if(self.tabs_added is False):

			self.ids.test_tabs.add_widget(Tab(text="gate-or"))
			self.ids.test_tabs.add_widget(Tab(text="gate-and"))
			self.ids.test_tabs.add_widget(Tab(text="gate-xor"))

			self.tabs_added = True

	def on_leave(self):
		if ( self.event ):
			self.event.cancel()

	def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
		'''Called when switching tabs.
		:type instance_tabs: <kivymd.uix.tab.MDTabs object>;
		:param instance_tab: <__main__.Tab object>;
		:param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
		:param tab_text: text or name icon of tab;
		'''
		#count_icon = [k for k, v in md_icons.items() if v == tab_text]
		#instance_tab.ids.icon.icon = count_icon[0]
		if (tab_text == "\uF8E4"):
			instance_tab.ids.content.text = " OR "
			if  self.event:
				self.event.cancel()
			self.event = Clock.schedule_interval(partial(self.or_gate,instance_tab), 1)
			

		elif(tab_text == "\uF8E6"):
			instance_tab.ids.content.text = " XOR "
			if  self.event:
				self.event.cancel()
			self.event = Clock.schedule_interval(partial(self.xor_gate,instance_tab), 1)

		elif(tab_text == "\uF8E0"):
			instance_tab.ids.content.text = " AND"
			if  self.event:
				self.event.cancel()
			self.event = Clock.schedule_interval(partial(self.and_gate,instance_tab), 1)

	def or_gate(self, instance_tab ,dt):
		self.counter[0] = self.counter[0] + 1
		if Hardware_data :
			text, icon_text = self.act1.or_gate() 
			text = "{} [{}]".format(text, self.counter[0])
		else:
			text = "{} [{}]".format(dt,self.counter[0])		
			icon_text = "school"
		
		instance_tab.ids.scroll.add_widget(LeftIconItem(text =text , icon = icon_text ))

	def xor_gate(self, instance_tab, dt):
		self.counter[1] = self.counter[1] + 1
		if Hardware_data :
			text, icon_text = self.act1.xor_gate() 
			text = "{} [{}]".format(text, self.counter[1])
		else:
			text = "{} [{}]".format(dt,self.counter[1])		
			icon_text = "school"
		
		instance_tab.ids.scroll.add_widget(LeftIconItem(text =text , icon = icon_text ))

	def and_gate(self, instance_tab, dt):
		self.counter[2] = self.counter[2] + 1
		if Hardware_data :
			text, icon_text = self.act1.and_gate() 
			text = "{} [{}]".format(text, self.counter[2])
		else:
			text = "{} [{}]".format(dt,self.counter[2])		
			icon_text = "school"
		
		instance_tab.ids.scroll.add_widget(LeftIconItem(text =text , icon = icon_text ))

#second screen
class SecondScreen(Screen):
	"""docstring for SecondScreen"""
	event = None
	toggle = True
	icon_left = None
	icon_right = None

	class Icon:
		on = None
		off = None

	def on_enter(self):
		self.icon_left = self.Icon()
		self.icon_right = self.Icon()

		self.icon_left.on = "arrow-left-bold"
		self.icon_left.on = "arrow-left-bold-outline"	
		self.icon_left.on = "arrow-right-bold"
		self.icon_left.on = "arrow-right-bold-outline"		

	def on_leave(self):
		if ( self.event ):
			self.event.cancel()
		self.event = None

	def button_press(self, direction):
		if( self.event ):
			self.event.cancel()

		self.event = Clock.schedule_interval(partial(self.blinker, direction ), 1)



	def blinker(self, direction, dt):
		"""
		"arrow-left-bold"
		"arrow-left-bold-outline"
		"arrow-right-bold-outline"
		"arrow-right-bold"
		"""
		if ( direction == "left"):
			#on
			self.icon_left.on = "arrow-left-bold"
			self.icon_right.on = "arrow-right-bold-outline"
			#off
			self.icon_left.off = "arrow-left-bold-outline"
			self.icon_right.off = "arrow-right-bold-outline"

		if (direction == "right"):
			#on
			self.icon_left.on = "arrow-left-bold-outline"
			self.icon_right.on = "arrow-right-bold"
			#off
			self.icon_left.off = "arrow-left-bold-outline"
			self.icon_right.off = "arrow-right-bold-outline"

		if (direction == "both"):
			#on
			self.icon_left.on = "arrow-left-bold"
			self.icon_right.on = "arrow-right-bold"
			#off
			self.icon_left.off = "arrow-left-bold-outline"
			self.icon_right.off = "arrow-right-bold-outline"

		if ( self.toggle ):
			self.toggle = False
			self.ids["left_b"].icon = self.icon_left.on
			self.ids["right_b"].icon = self.icon_right.on
			print ( "turn on" )
		else:
			self.toggle = True
			self.ids["left_b"].icon = self.icon_left.off
			self.ids["right_b"].icon = self.icon_right.off
			print ("turn off")

#second screen
class ThirdScreen(Screen):
	increasing = NumericProperty(1)
	begin = NumericProperty(50)
	step = NumericProperty(1)
	event = None

	if Hardware_data:
		act3 = ThirdActivity()
		sampling = NumericProperty(0)
		value = NumericProperty(0)

	def on_enter(self):
        #box = BoxLayout(orientation='horizontal', padding=5)
		self.ids.box.clear_widgets() # remove widgets
		self.gauge1 = Gauge(value=50, size_gauge=256, size_text=25)
		self.gauge2 = Gauge(value=50, size_gauge=256, size_text=25)
		#self.slider = Slider(orientation='vertical')
		self.gauge1.pos_hint = {'x': 0.15, 'y': 0.5}
		self.gauge2.pos_hint = {'x': 0.5, 'y': 0.5}
		#stepper = Slider(min=1, max=25)
		#stepper.bind(
		#    value=lambda instance, value: setattr(self, 'step', value)
		#)

		self.ids.box.add_widget(self.gauge1)
		self.ids.box.add_widget(self.gauge2)
		#self.ids.box.add_widget(stepper)
		#self.ids.box.add_widget(self.slider)
		self.event = Clock.schedule_interval(lambda *t: self.gauge_increment(), 0.03)


	def on_leave(self):
		self.event.cancel()

	def gauge_increment(self):

		if Hardware_data:
			if( self.sampling < 5):
				self.value = self.act3.read_ch() + self.value
				self.sampling += 1 
			else:
				self.gauge1.value = self.rpm_adc_conversion(self.value/self.sampling)
				self.gauge2.value = 100 - self.rpm_adc_conversion(self.value/self.sampling)
				self.sampling = 1
				self.value = 0
		else:
			begin = self.begin
			begin += self.step * self.increasing
			if begin > 0 and begin < 100:
				self.gauge1.value = begin
				self.gauge2.value = begin
			else:
				self.increasing *= -1
			self.begin = begin

	def rpm_adc_conversion(self, adc):
		"""
			m = (y2 - y1) / (x2 - x1)
			y2 = (x2-x1)*m + y1
			p1 ( x1, y1 ) -> (0 adc counts, 0 rpm)
			p2 ( x2, y2 ) -> (65535 adc coutns, 100 rpm)
			y2 = (x2 - 0 )* (100 - 0 ) / (65535 - 0 ) + 0
			rpm = adc * (100/65535)
		"""
		rpm = 0

		if adc > 52000:
			rpm = 100
		else:
			rpm = adc*(100/52000)

		return rpm

class FourthScreen(Screen):

	dialog = None

	def on_enter(self):
		if self.dialog is None:
			self.dialog = MDDialog(
				title = "Error",
				text = "Server error, it might be out of the network. Please make sure is reachable.",
				buttons = [
					MDFlatButton(text = "OK", on_release = self.dismiss_dialog)
				],
				)

	def request_turn_on(self):
		try:
			r = requests.get('http://rb-desktop.local:5000/api/v0.1/gpiod4/True',timeout=5)
		except requests.exceptions.RequestException as e:
			self.ids.server_status.text = "Connection Error"
			self.dialog.open()
			print( e )
		else:
			self.ids.server_status.text = r.text

	def request_turn_off(self):
		try:
			r = requests.get('http://rb-desktop.local:5000/api/v0.1/gpiod4/False',timeout=5)
		except requests.exceptions.RequestException as e:
			self.ids.server_status.text = "Connection Error"
			self.dialog.open()
			print( e )
		else:
			self.ids.server_status.text = r.text


	def api_status(self):
		try:
			r = requests.get('http://rb-desktop.local:5000/api/v0.1/api_status',timeout=5)
		except requests.exceptions.RequestException as e:
			self.ids.server_status.text = "Connection Error"
			self.dialog.open()
			print( e )
		else:
			self.ids.server_status.text = r.text

	def dismiss_dialog(self):
		self.dialog.dismiss()

class FifthScreen(Screen):

	logged = False

	if Hardware_data:
		act5 = FifthActivity()

	def on_enter(self):
		with open('userdatabase.json') as file:
			self.data = json.load(file)

		self.sound_wrong = sa.WaveObject.from_wave_file('wrong.wav')
		self.sound_success = sa.WaveObject.from_wave_file('success.wav')
	
	def signin(self):

		# print ( self.data )

		if ( len(self.ids.username.text) == 0  ):
			toast("Username need to be entered")
			self.logged = False
		else:
			if( len(self.ids.password.text) == 0 ):
				toast("Password need to be entered")
				self.logged = False
			else:
				for user in self.data['users']:
					if (user['username'] == self.ids.username.text):
						if (user['password'] == self.ids.password.text):
							self.logged = True
							break
						else:
							self.logged = False
					else:
						self.logged = False

		if (self.logged):
			self.ids.result.text = "Successfuly logged in"
			self.ids.result.theme_text_color = 'Custom'
			self.ids.result.text_color = rgba(0,255,0,255)
			self.sound_success.play()
			if Hardware_data:
				self.act5.LoggedIn()
		else:
			self.ids.result.text = "Wrog password or username"
			self.ids.result.theme_text_color = 'Error'
			self.sound_wrong.play()
			if Hardware_data:
				self.act5.WrogLogIn()

#sixth Screen
class SixthScreen(Screen):

	from Activities.sixth_activity import Commands

	text_led = ["Red", "Green", "Blue"]

	# def on_enter(self):
	# 	for i in range(3):
	# 		self.ids.list_led.add_widget(ListItemWithCheckbox(text= self.text_led[i] + " Led", icon="led-on"))

	def on_check_box_active(self, cb_name ,checkbox,value):

		if value:
			if cb_name == 'red':
				cmd = self.Commands.CMD_TURN_ON_RED.send
				name = self.Commands.CMD_TURN_ON_RED.name
			if cb_name == 'blue':
				cmd = self.Commands.CMD_TURN_ON_BLUE.send
				name = self.Commands.CMD_TURN_ON_BLUE.name
			if cb_name == 'green':
				cmd = self.Commands.CMD_TURN_ON_GREEN.send
				name = self.Commands.CMD_TURN_ON_GREEN.name
		else:
			if cb_name == 'red':
				cmd = self.Commands.CMD_TURN_OFF_RED.send
				name = self.Commands.CMD_TURN_OFF_RED.name
			if cb_name == 'blue':
				cmd = self.Commands.CMD_TURN_OFF_BLUE.send
				name = self.Commands.CMD_TURN_OFF_BLUE.name
			if cb_name == 'green':
				cmd = self.Commands.CMD_TURN_OFF_GREEN.send
				name = self.Commands.CMD_TURN_OFF_GREEN.name

		print ( "led: {} - cmd resp: {} - cmd name: {}".format(cb_name,cmd,name))	

class SeventhScreen(Screen):

	# def on_pre_enter(self):
	# 	providers = ()
	# 	providers += (('picamera', 'camera_picamera', 'CameraPiCamera'), )
	# 	providers += (('gi', 'camera_gi', 'CameraGi'), )
	# 	providers += (('opencv', 'camera_opencv', 'CameraOpenCV'), )
	# 	Camera = core_select_lib('camera', (providers))

	def on_enter(self):
		self.cam = Camera(play=False, resolution = (640, 480))
		self.ids.cambox.add_widget(self.cam)

	def capture(self):
		timestr = time.strftime("%Y%m%d_%H%M%S")
		self.cam.export_to_png("IMG_{}.png".format(timestr))
		print("capture")

	def play(self):
		self.cam.play = not self.cam.play 
		print ("play")

	def on_leave(self):
		self.cam.play = False
		self.ids.cambox.remove_widget(self.cam)


class EigthScreen(Screen):

	my_camera = None
	

	def on_enter(self):

		if not Hardware_data:
			self.capture = cv2.VideoCapture(0)
			self.my_camera = KivyCamera(capture=self.capture, fps=30)
			self.ids.box.add_widget(self.my_camera)

	def on_leave(self):
		self.capture.release()
		self.my_camera.stop()
		self.ids.box.remove_widget(self.my_camera)

	def face_detection(self):
		self.my_camera.mode( True )

	def face_recognition(self):
		self.my_camera.mode( False )

#About me activity
class AboutMe(Screen):
	simple_dialog = None
	read_file = False

	def on_enter(self):

		if self.read_file is False:
			f = open("bibliography.txt","r")
			self.ids.biography.text = f.read()
			self.read_file = True

		if not self.simple_dialog:
			self.simple_dialog = MDDialog(
				title="Contanct Me",
				type="simple",
				items=[
				AvatarItem(
					text="romy.bompartbll@uanl.edu.mx",
					source="romybompart.png",
					),
				LeftIconItem(
					text="+52 1 811 802 76 53",
					icon="cellphone",
					),
				],
			)
			self.simple_dialog.open()
			self.simple_dialog = None

#Main App
class Main(MDApp):
	"""docstring for Main"""
	title = "Embedded Systems"

	def build(self):
		self.theme_cls.primary_palette = "Green"
		self.theme_cls.theme_style = "Light"
		return Builder.load_file("main.kv")

	def on_start(self):
		if not Hardware_data:
			self.root.ids.webserver.disabled = False

#App starting
if __name__ == '__main__':
	Application = Main()
	Application.run()
