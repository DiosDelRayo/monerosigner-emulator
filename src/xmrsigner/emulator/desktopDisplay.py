######################################################################
#  Work based on:
#  Seedsigner desktop display driver and button emulator
#  by: @EnteroPositivo (Twitter, Gmail, GitHub)
from time import sleep, time

from .webcamvideostream import WebcamVideoStream
from xmrsigner.emulator.virtualGPIO import GPIO
from xmrsigner.hardware.buttons import HardwareButtons
from xmrsigner.resources import get as res
from xmrsigner.hardware.camera import Camera, CameraMode
from .capturewindow import TransparentCaptureWindow
from .recorder import ScreenRecorder

from tkinter import *
import tkinter as tk
# from tkinter import ttk


from PIL import Image, ImageTk

import threading
import os
from typing import Optional
from sys import exit
from typing import List


EMULATOR_VERSION = '0.4.7'
VIRTUAL_SCREEN_CAM = 'vScreen'


class desktopDisplay(threading.Thread):
    """class for desktop display."""

    root=0
    recording: bool = False

    def __init__(self):
        self.width = 240
        self.height = 240
        self.available_cameras: List[int] = [] 
        self.recorder: ScreenRecorder = ScreenRecorder('xmrsigner-{{ timestamp }}.gif')

        # Multithreading
        threading.Thread.__init__(self)
        self.start()

        from xmrsigner.models.threads import BaseThread
        from xmrsigner.gui.screens.screen import PowerOffScreen
        from xmrsigner.views import view
        class PowerOffView(view.View):
            def run(self):
                thread = PowerOffView.PowerOffThread()
                thread.start()
                PowerOffScreen().display()


            class PowerOffThread(BaseThread):
                def run(self):
                    from subprocess import call
                    while self.keep_running:
                        sleep(10)
                        call("kill $(ps aux | grep '[p]ython.*main.py' | awk '{print $2}')", shell=True)


        # patch power off, to not power off the machine
        view.PowerOffView = PowerOffView
        self.capture_window = None
        self.capture_window_visible = False

    def callback(self):
        self.root.quit()
        self.root.destroy()
        # terminate the main thread forcefully
        pid = os.getpid()
        os.kill(pid,9)

    def run(self):
        """run thread"""    
        self.root = tk.Tk()

        from xmrsigner.controller import Controller
        controller = Controller.get_instance()
        title_term = "XmrSigner Emulator v"+EMULATOR_VERSION+ " / "+controller.VERSION;
        title= "XmrSigner"

        print("*****************************************************");
        print(title_term);
        print("https://github.com/DiosDelRayo/monerosigner-emulator");
        print("*****************************************************");

        self.root.title(title)

        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.geometry("480x260+240+240")
        self.root.maxsize(480, 260)
        self.root.minsize(480, 260)
        self.root.resizable(0, 0)
        self.root.configure(bg='#ED5F00')
        self.root.iconphoto(False, tk.PhotoImage(data=res('icons', 'logo_black_64.png')))

        self.label=Label(self.root)
        self.label.pack()

        self.joystick=Frame(self.root)
        self.joystick.pack()
        self.joystick.place(x=20, y=85)
        self.joystick.configure(bg='#ED5F00')

        pixel = tk.PhotoImage(width=1, height=1)


        self.btnL = Button(self.joystick, image=pixel,  width=20, height=20,  command = HardwareButtons.KEY_LEFT_PIN, bg='black')
        self.btnL.grid(row=1, column=0)
        self.bindButtonClick(self.btnL)

        self.btnR = Button(self.joystick, image=pixel,  width=20, height=20, command = HardwareButtons.KEY_RIGHT_PIN, bg='black')
        self.btnR.grid(row=1, column=2)
        self.bindButtonClick(self.btnR)

        self.btnC = Button(self.joystick, image=pixel,  width=20, height=20, command = HardwareButtons.KEY_PRESS_PIN, bg='#2C2C2C')
        self.btnC.grid(row=1, column=1)
        self.bindButtonClick(self.btnC)

        self.btnU = Button(self.joystick, image=pixel,  width=20, height=20, command = HardwareButtons.KEY_UP_PIN, bg='black')
        self.btnU.grid(row=0, column=1)
        self.bindButtonClick(self.btnU)

        self.btnD = Button(self.joystick, image=pixel,  width=20, height=20, command = HardwareButtons.KEY_DOWN_PIN, bg='black')
        self.btnD.grid(row=2, column=1)
        self.bindButtonClick(self.btnD)

        self.btn1 = Button(self.root, image=pixel,  width=40, height=20,  command = HardwareButtons.KEY1_PIN, bg='black')
        self.btn1.place(x=400, y=60)
        self.bindButtonClick(self.btn1)

        self.btn2 = Button(self.root, image=pixel,  width=40, height=20,  command = HardwareButtons.KEY2_PIN, bg='black')
        self.btn2.place(x=400, y=116)
        self.bindButtonClick(self.btn2)

        self.btn3 = Button(self.root, image=pixel,  width=40, height=20,  command = HardwareButtons.KEY3_PIN, bg='black')
        self.btn3.place(x=400, y=172)
        self.bindButtonClick(self.btn3)

        self.set_available_cameras(WebcamVideoStream.list_available_cameras())

        def key_handler(event):

            if(event.keysym=="Up"): GPIO.set_input(HardwareButtons.KEY_UP_PIN, GPIO.HIGH)
            if(event.keysym=="Down"): GPIO.set_input(HardwareButtons.KEY_DOWN_PIN, GPIO.HIGH)
            if(event.keysym=="Left"): GPIO.set_input(HardwareButtons.KEY_LEFT_PIN, GPIO.HIGH)
            if(event.keysym=="Right"): GPIO.set_input(HardwareButtons.KEY_RIGHT_PIN, GPIO.HIGH)

            if(event.keysym in ("1", "KP_1") ): GPIO.set_input(HardwareButtons.KEY1_PIN, GPIO.HIGH)
            if(event.keysym in ("2", "KP_2") ): GPIO.set_input(HardwareButtons.KEY2_PIN, GPIO.HIGH)
            if(event.keysym in ("3", "KP_3") ): GPIO.set_input(HardwareButtons.KEY3_PIN, GPIO.HIGH)

            if(event.keysym=="Return"): GPIO.set_input(HardwareButtons.KEY_PRESS_PIN, GPIO.HIGH)

        self.root.bind("<Key>", key_handler)

        self.btnRecord = Button(self.root, text="○", command=self.record_toggle, bg='#ED5F00', fg='#FFFFFF')
        self.btnRecord.place(x=10, y=210)


        # Add a toggle button for the capture window
        self.capture_window_btn = Button(self.root, text="Area", command=self.toggle_capture_window)
        self.capture_window_btn.place(x=10, y=50)
        self.capture_window_btn.config(width=7, bg='#ED5F00', fg='#FFFFFF')

        # Create the transparent capture window
        self.capture_window = TransparentCaptureWindow(self.root, Camera.get_instance().monitor)

        self.root.resizable(width = True, height = True)
        self.root.mainloop()


    def bindButtonClick(self, objBtn):
        objBtn.bind("<Button>", self.buttonDown)
        objBtn.bind("<ButtonRelease>", self.buttonUp)

    def buttonDown(self, objBtn):
        gpioID = (objBtn.widget.config('command')[-1])
        GPIO.set_input(gpioID, GPIO.HIGH)

    def buttonUp(self, objBtn):
        gpioID = (objBtn.widget.config('command')[-1])
        GPIO.set_input(gpioID, GPIO.LOW)   

    def setGPIO(self, pin):
        GPIO.fire_raise_event(pin)

    def ShowImage(self, Image2, Xstart, Ystart) -> None:
        while(self.root==0): sleep(0.1)
        imwidth, imheight = Image2.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display \
                    ({0}x{1}).' .format(self.width, self.height))
        self.recorder.record_frame(Image2)

        self.tkimage = ImageTk.PhotoImage(Image2, master=self.root)
        self.label.configure(image=self.tkimage)
        self.label.image=self.tkimage
        self.label.place(x=125, y=10)

    def clear(self):
        """Clear contents of image buffer"""

    def toggle_capture_window(self):
        if Camera.get_instance().is_active():
            self.capture_window.toggle()
            self.capture_window_visible = not self.capture_window_visible
        else:
            print("Camera is not active. Cannot show capture window.")

    def set_available_cameras(self, camera_list: List[int]):
        print(camera_list)
        self.available_cameras = camera_list
        if len(self.available_cameras) > 0:
            self.show_camera_dropdown_list()

    def update_default_camera(self, *args):
        camera = self.camera_var.get()
        if camera == VIRTUAL_SCREEN_CAM:
            Camera.get_instance().set_mode(CameraMode.Screen)
            if self.capture_window_visible:
                self.capture_window.show()
        else:
            Camera.get_instance().set_mode(CameraMode.WebCam)
            WebcamVideoStream.set_default_camera(int(camera))
            self.capture_window.hide()
            self.capture_window_visible = False

    def show_camera_dropdown_list(self):
        self.camera_var = tk.StringVar(self.root)
        self.camera_var.set(self.available_cameras[0])
        self.camera_dropdown = tk.OptionMenu(self.root, self.camera_var, VIRTUAL_SCREEN_CAM, *self.available_cameras)
        self.camera_dropdown.config(width=5, bg='#ED5F00', fg='#FFFFFF')
        self.camera_dropdown.place(x=10, y=10)
        self.camera_var.trace('w', self.update_default_camera)

    def record_toggle(self):
        if self.recorder.recording:
            self.recorder.stop()
            self.btnRecord.config(text="○")  # Change caption to circle
        else:
            self.recorder.record()
            self.btnRecord.config(text="■")  # Change caption to square
