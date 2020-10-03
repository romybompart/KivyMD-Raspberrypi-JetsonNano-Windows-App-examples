# Kivy Material Design (KivyMD) for Multi environment system
============================

 This project explores the use of KivyMD to implement several 
 examples in three different hardwares: 

 1. Acer E5-575-33B, Intel Core i3 7th Gen using windows 10
 2. Jetson Nano, Maxwell GPU/ARM Cortex-A57 MPCore, Ubuntu 18.04
 3. Raspberry pi 4

 The modules that can be found in the project: 

 * Digital gates:
 ⋅⋅⋅ Read GPIO inputs in a Raspberry pi or in a Jetson nano, and implment
 AND, OR and XOR logics. The information is presented in separated tabs, 
 the data is adquired each second depending on the tab, and it is included
 in the view as a list. When the list is greater than the screen, provides
 an scroll. For Windows in just record the timestamp and provide the info
 in the tab page that was selected. 

 * Blinkers:
 ⋅⋅⋅ Implement a window that can simulate the blinkers in a car. This is 
 implemented using the buttons from Material Desing. They are changed to
 make the impresion the blinkers are turning on and turning off. 

 * Rotate Image:
 ⋅⋅⋅ Using a custom widget create in KivyMD is possible to rotate a needle 
 in front of an applique that simulates the speedo or a car gauge 
 indicator, the rotation of the needle is possible using a potetiometer 
 connected to a MCP3008 by SPI to the Jetson Nano or the Raspberry pi. 
 For the Windows interface this will be moving automatically. 

 * Web Server:
 ⋅⋅⋅ For windows, provides an interface to request web services to a remote server (jetson nano or raspbery pi ). The server script that need to be run in order to visualize the interaction between the client (windows computer) and the server (Raspberry pi or Jetson nano) is in the folder Activities and inside of JetsonApiRest.py 
 ⋅⋅⋅ The idea is to start the service (Run JetsonApiRest.py), then click \
 on the buttons provided in the kivy interface, and check the label value
 which is the server response. 
 ⋅⋅⋅ The possible requests are turn on a LED , turn off a LED and check 
 the api status.
 ⋅⋅⋅ This interface in Linux devices: Raspberry pi, jetson nano or Linux 
 desktop computers. 

 * Form
 ⋅⋅⋅ Emulating a Login form, the passwords and the user names are stored in
 the userdatabase.json . In the raspberry pi and jetson nano platform 
 When the user introduces a correct password the interfaces shows a green 
 label of success and turns on a LED, if it is not correct the label 
 changes to red and display a wrong message , additionally the LED is 
 turned off. 
  ⋅⋅⋅ In a windows computer, if correct it reproduces a sound of success, 
  and when it is not correct reproduces a sound of invalid credentials.

 * PSOC SPI
 ⋅⋅⋅ This is to interface with a PSOC 4200, but it can be an arduino, or 
 any other device with SPI. The idea is to click on the checker boxes to 
 command turn on a color of a RGB LED. These checker boxes are toogle type
 so only one can be pressed at the time. For a Wiwndows interface it only
 provide a debuging in the console about the intended command to be send. 

 * Camera (windows only)
⋅⋅⋅ Using the Camera widget of to check the capabilities.
Please do not use this on raspberry pi yet, the raspberry pi cam hasn't
been implmented yet nor the GSTREAMER camera configuration from the Jetson

* OPENCV (windows only)
⋅⋅⋅ Using opencv now we have control of the output image, so we can make 
image processing, in this case I implemented two cases: face detection
and face recognition. I am using the same idea from the [Raspberry Pi Face Recognition](https://www.pyimagesearch.com/2018/06/25/raspberry-pi-face-recognition/) from @jrosebr1. 

* About Me
⋅⋅⋅ A pop up message will prompt at the screen the first time the page is 
loaded, after the user click on any side of the screen outside of the 
message, you are going to be able to read a brief biography loaded from a 
bibliography.txt

#The Hardware connection
============================
TODO

