#from picamera import PiCamera
from PIL import Image
#from xmrsigner.hardware.pivideostream import PiVideoStream
from xmrsigner.emulator.webcamvideostream import WebcamVideoStream
from xmrsigner.emulator.screencapture import ScreenCapture, Monitor
from xmrsigner.models.settings import Settings, SettingsConstants
from xmrsigner.models.singleton import Singleton
from enum import Enum


class CameraMode(Enum):
    Screen = 1
    WebCam = 2


class Camera(Singleton):
    _video_stream = None
    _picamera = None
    _screen_capture = None
    _camera_rotation = None
    _current_mode: CameraMode = CameraMode.WebCam
    _monitor: Monitor = None

    @classmethod
    def get_instance(cls):
        # This is the only way to access the one and only Controller
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        cls._instance._camera_rotation = int(Settings.get_instance().get_value(SettingsConstants.SETTING__CAMERA_ROTATION))
        cls._instance._monitor = Monitor(width=512, height=384)
        return cls._instance


    def start_video_stream_mode(self, resolution=(512, 384), framerate=12, format='bgr'):
        if self._video_stream is not None or self._screen_capture is not None:
            self.stop_video_stream_mode()

        if self._current_mode == CameraMode.WebCam:
            self._video_stream = WebcamVideoStream(resolution=resolution, framerate=framerate, format=format)
            self._video_stream.start()
        elif self._current_mode == CameraMode.Screen:
            self._monitor = self._monitor
            self._screen_capture = ScreenCapture(monitor=self._monitor, framerate=framerate)
            self._screen_capture.start()
        else:
            raise ValueError("Invalid mode. Choose 'webcam' or 'screen'.")

    def read_video_stream(self, as_image=False):
        if self._current_mode == CameraMode.WebCam:
            if not self._video_stream:
                raise Exception("Must call start_video_stream first.")
            if not self._video_stream.hasCamera():
                raise Exception("Can not open Webcam")
            frame = self._video_stream.read()
        elif self._current_mode == CameraMode.Screen:
            if not self._screen_capture:
                raise Exception("Must call start_video_stream first.")
            frame = self._screen_capture.read()
        else:
            raise Exception('No active video stream.')


        if not as_image:
            return frame
        else:
            if frame is not None:
                return Image.fromarray(frame.astype('uint8'), 'RGB').rotate(90 + self._camera_rotation)
        return None


    def stop_video_stream_mode(self):
        if self._video_stream is not None:
            self._video_stream.stop()
            self._video_stream = None
        if self._screen_capture is not None:
            self._screen_capture.stop()
            self._screen_capture = None

    def start_single_frame_mode(self, resolution=(720, 480)):
        if self._video_stream is not None:
            self.stop_video_stream_mode()
        if self._picamera is not None:
            self._picamera.close()


    def capture_frame(self):
        if self._current_mode == CameraMode.WebCam:
            frame = WebcamVideoStream.single_frame()
        elif self._current_mode == CameraMode.Screen:
            frame = ScreenCapture.single_frame(self._monitor)
        else:
            raise Exception('Invalid mode.')
        return Image.fromarray(frame).rotate(90 + self._camera_rotation)


    def stop_single_frame_mode(self):
        if self._picamera is not None:
            self._picamera.close()
            self._picamera = None

    def set_mode(self, mode: CameraMode) -> None:
        self._current_mode = mode

    @property
    def mode(self) -> CameraMode:
        return self._current_mode

    @property
    def monitor(self) -> Monitor:
        return self._monitor

    def is_active(self):
        return self._current_mode == CameraMode.Screen
