import sys
from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QFrame, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PIL import Image, ImageQt
from time import sleep

from xmrsigner.emulator.virtualGPIO import GPIO
from xmrsigner.hardware.buttons import HardwareButtons
from xmrsigner.resources import get as res
from xmrsigner.hardware.camera import Camera, CameraMode
from .capturewindow import TransparentCaptureWindow

from typing import Optional

EMULATOR_VERSION = '0.4.5'
VIRTUAL_SCREEN_CAM = 'vScreen'

class DesktopDisplay(QMainWindow, QThread):
    image_updated = pyqtSignal(QPixmap)

    def __init__(self):
        super().__init__()
        QThread.__init__(self)
        self.width = 240
        self.height = 240
        self.available_cameras = []
        self.capture_window = None
        self.capture_window_visible = False
        self.init_ui()
        self.start()

    def init_ui(self):
        # Set up main window
        self.setWindowTitle("XmrSigner")
        self.setGeometry(240, 240, 480, 260)
        self.setFixedSize(480, 260)
        self.setStyleSheet("background-color: #ED5F00;")

        # Set up layout
        main_layout = QVBoxLayout()
        self.central_widget = QFrame(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(main_layout)

        # Image label
        self.label = QLabel(self)
        main_layout.addWidget(self.label)

        # Joystick frame
        joystick_frame = QFrame(self)
        joystick_layout = QVBoxLayout()
        joystick_frame.setLayout(joystick_layout)

        # Joystick buttons
        self.btnU = self.create_button(HardwareButtons.KEY_UP_PIN)
        self.btnL = self.create_button(HardwareButtons.KEY_LEFT_PIN)
        self.btnC = self.create_button(HardwareButtons.KEY_PRESS_PIN)
        self.btnR = self.create_button(HardwareButtons.KEY_RIGHT_PIN)
        self.btnD = self.create_button(HardwareButtons.KEY_DOWN_PIN)

        # Arrange joystick buttons
        joystick_layout.addWidget(self.btnU, alignment=Qt.AlignCenter)
        middle_row = QHBoxLayout()
        middle_row.addWidget(self.btnL)
        middle_row.addWidget(self.btnC)
        middle_row.addWidget(self.btnR)
        joystick_layout.addLayout(middle_row)
        joystick_layout.addWidget(self.btnD, alignment=Qt.AlignCenter)

        main_layout.addWidget(joystick_frame)

        # Side buttons
        self.btn1 = self.create_button(HardwareButtons.KEY1_PIN)
        self.btn2 = self.create_button(HardwareButtons.KEY2_PIN)
        self.btn3 = self.create_button(HardwareButtons.KEY3_PIN)

        # Position side buttons
        self.btn1.move(400, 60)
        self.btn2.move(400, 116)
        self.btn3.move(400, 172)

        # Capture window toggle button
        self.capture_window_btn = QPushButton("Toggle Capture Window", self)
        self.capture_window_btn.clicked.connect(self.toggle_capture_window)
        self.capture_window_btn.move(10, 50)

        # Camera dropdown
        self.camera_dropdown = QComboBox(self)
        self.camera_dropdown.move(10, 10)
        self.camera_dropdown.currentTextChanged.connect(self.update_default_camera)

        self.image_updated.connect(self.update_image)

    def create_button(self, command):
        button = QPushButton(self)
        button.setFixedSize(20, 20)
        button.setStyleSheet("background-color: black;")
        button.pressed.connect(lambda: self.button_pressed(command))
        button.released.connect(lambda: self.button_released(command))
        return button

    def button_pressed(self, command):
        GPIO.set_input(command, GPIO.HIGH)

    def button_released(self, command):
        GPIO.set_input(command, GPIO.LOW)

    def run(self):
        # Thread logic here
        pass

    def ShowImage(self, image, x_start, y_start):
        q_image = ImageQt.ImageQt(image)
        pixmap = QPixmap.fromImage(q_image)
        self.image_updated.emit(pixmap)

    def update_image(self, pixmap):
        self.label.setPixmap(pixmap)
        self.label.move(125, 10)

    def toggle_capture_window(self):
        if Camera.get_instance().is_active():
            if self.capture_window:
                self.capture_window.toggle()
            self.capture_window_visible = not self.capture_window_visible
        else:
            print("Camera is not active. Cannot show capture window.")

    def set_available_cameras(self, camera_list):
        self.available_cameras = camera_list
        if len(self.available_cameras) > 0:
            self.show_camera_dropdown_list()

    def update_default_camera(self, camera):
        if camera == VIRTUAL_SCREEN_CAM:
            Camera.get_instance().set_mode(CameraMode.Screen)
            if self.capture_window_visible and self.capture_window:
                self.capture_window.show()
        else:
            Camera.get_instance().set_mode(CameraMode.WebCam)
            WebcamVideoStream.set_default_camera(int(camera))
            if self.capture_window:
                self.capture_window.hide()
            self.capture_window_visible = False

    def show_camera_dropdown_list(self):
        self.camera_dropdown.clear()
        self.camera_dropdown.addItem(VIRTUAL_SCREEN_CAM)
        for camera in self.available_cameras:
            self.camera_dropdown.addItem(str(camera))

    def keyPressEvent(self, event):
        key_map = {
            Qt.Key_Up: HardwareButtons.KEY_UP_PIN,
            Qt.Key_Down: HardwareButtons.KEY_DOWN_PIN,
            Qt.Key_Left: HardwareButtons.KEY_LEFT_PIN,
            Qt.Key_Right: HardwareButtons.KEY_RIGHT_PIN,
            Qt.Key_1: HardwareButtons.KEY1_PIN,
            Qt.Key_2: HardwareButtons.KEY2_PIN,
            Qt.Key_3: HardwareButtons.KEY3_PIN,
            Qt.Key_Return: HardwareButtons.KEY_PRESS_PIN,
        }
        if event.key() in key_map:
            GPIO.set_input(key_map[event.key()], GPIO.HIGH)

    def keyReleaseEvent(self, event):
        key_map = {
            Qt.Key_Up: HardwareButtons.KEY_UP_PIN,
            Qt.Key_Down: HardwareButtons.KEY_DOWN_PIN,
            Qt.Key_Left: HardwareButtons.KEY_LEFT_PIN,
            Qt.Key_Right: HardwareButtons.KEY_RIGHT_PIN,
            Qt.Key_1: HardwareButtons.KEY1_PIN,
            Qt.Key_2: HardwareButtons.KEY2_PIN,
            Qt.Key_3: HardwareButtons.KEY3_PIN,
            Qt.Key_Return: HardwareButtons.KEY_PRESS_PIN,
        }
        if event.key() in key_map:
            GPIO.set_input(key_map[event.key()], GPIO.LOW)
