from threading import Thread
import time
import cv2
from typing import List, Tuple, Optional


class WebcamVideoStream:

    default_camera: int = 0

    def __init__(self, resolution=(320, 240), framerate: int = 32, format: str = 'bgr', camera: Optional[int] = None, **kwargs):
        # initialize the camera
        if not camera:
            camera = self.default_camera

        print(f'Using camera {camera}...')
        self.camera = cv2.VideoCapture(camera)
        self.set_resolution(resolution)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.should_stop = False
        self.is_stopped = True

    def start(self) -> bool:
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        self.is_stopped = False
        return self

    def hasCamera(self) -> bool:
        return self.camera.isOpened()

    def update(self) -> None:
        if self.hasCamera():
            # keep looping infinitely until the thread is stopped
            while(not self.should_stop):
                # grab the frame from the stream and clear the stream in
                # preparation for the next frame
                ret, stream = self.camera.read()
                stream = cv2.resize(stream, (240,240))
                stream = cv2.cvtColor(stream,cv2.COLOR_BGR2RGB)
                time.sleep(0.05)
                self.frame = stream

            self.is_stopped = True
            self.should_stop = False
            return

        else:
            self.is_stopped = True
            self.should_stop = False
            return



    def read(self):
        return self.frame

    def single_frame(camera: Optional[int] = None):
        if not camera:
            camera = WebcamVideoStream.default_camera
        print(f'Using camera {camera} for still picture')
        cap = cv2.VideoCapture(camera)
        ret, frame = cap.read()
        return frame

    def stop(self) -> None:
        # indicate that the thread should be stopped
        self.should_stop = True
        # Block in this thread until stopped
        while not self.is_stopped:
            pass

    def set_resolution(self, resolution: Tuple[int, int]):
        self.camera.set(3, resolution[0])
        self.camera.set(4, resolution[1])	

    @staticmethod
    def list_available_cameras(max_cams_to_try: int = 10) -> List[int]:
        index = 0
        all_cams = []
        while index < max_cams_to_try:
            print(f'Check for camera: {index}...')
            try:
                cap = cv2.VideoCapture(index)
                if cap.isOpened():
                    all_cams.append(index)
                    cap.release()
            except:
                pass
            index += 1
        return all_cams

    @classmethod
    def set_default_camera(cls, camera: Optional[int] = None) -> None:
        print(f'Changed default camera to: {camera}')
        cls.default_camera = camera if camera is not None else 0
