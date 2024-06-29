from numpy import array as np_array
from dataclasses import dataclass
from cv2 import cvtColor, COLOR_RGBA2RGB
from mss import mss
from threading import Thread
from time import sleep
from typing import Dict, Tuple, Optional

from .streamdevice import StreamInputDevice


@dataclass
class Monitor:

    top: int = 0
    left: int = 0
    width: int = 320
    height: int = 240
    zoom: float = 1.0
    screen_width: int = 1920
    screen_height: int = 1080

    def set_screen_resolution(self, width, height) -> None:
        self.screen_width = width
        self.screen_height = height

    def center(self) -> Tuple[int, int]:
        return (self.left + int((self.width * self.zoom) // 2), self.top + int((self.height * self.zoom) // 2))

    def xy(self, center: Optional[Tuple[int, int]], width: Optional[int] = None, height: Optional[int] = None, zoom: Optional[int]) -> Tuple[int, int]:
        x, y = center or (self.left, self.top)
        w = width or self.width
        h = height or self.height
        z = zoom or self.zoom
        return (x - int(w * z), y - int(h * z))

    def correct_xy(self, x: int, y: int, zoom: Optional[int] = None) -> Tuple[int, int]:
        z = zoom or self.zoom
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if (x + int(self.width * z)) > self.screen_width:
            x = self.screen_width - int(self.width * z)
        if (y + int(self.height * z)) > self.screen_height:
            y = self.screen_height - int(self.height * z)
        return (x, y)

    def native_resolution(self) -> Tuple[int, int]:
        return (self.width, self.height)

    def zoom_resolution(self) -> Tuple[int, int]:
        return (int(self.width * self.zoom), int(self.height * self.zoom))

    def cords(
        self,
        left: Optional[int] = None,
        top: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        zoom: Optional[int] = None
    ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return (((left or self.left), top or self.top), (left or self.left + int((width or self.width) * (zoom or self.zoom)), (top or self.top) + int((height or self.height) * (zoom or self.zoom))))

    def is_coord_in_screen(self, x: int, y: int) -> bool:
        return 0 <= x <= self.screen_width and 0 <= y self.screen_height

    def are_coords_in_screen(self, coords: Tuple[Tuple[int, int], Tuple[int, int]]) -> bool:
        return self.is_coord_in_screen(coords[0][0], coords[0][1]) and self.is_coord_in_screen(coords[1][0], coords[1][1])

    def rectangle(self) -> Tuple[int, int, int, int]:
        return (self.top, self.left, int(self.width * self.zoom), int(self.height * self.zoom))

    def adjust_zoom(self, zoom_level: float = 1.0, use_max: bool = True) -> bool:
        if zoom_level < 0.1:
            if use_max:
                zoom_level = 0.1
            else
                return False

        if int(self.width * zoom_level) > self.screen_width or int(self.height * zoom_level) > self.screen_height:
            if not use_max:
                return False  # we can not zoom out of the screen, rectangle doesn't fit into the screen
            else:  # calculate max zoom level
                zoom_level = min(self.screen_width // self.width, self.screen_height // self.height)

        x, y = self.xy(self.center(), zoom=zoom_level)
        x, y = self.correct_xy(x, y, zoom_level)

        if self.are_coords_in_screen(self.coords(left=x, top=y, zoom=zoom_level)):
            self.top = y
            self.left = x
            self.zoom = zoom_level
            return True
        return False

    def move_to_xy(self, x: int, y: int, use_max: bool = False) -> bool:
        if self.are_coords_in_screen(self.coords(left=x, top=y)):
            self.left, self.top = (x, y)
            return True
        if use_max:
            self.left, self.top = self.correct_xy(x, y)
            return True
        return False

    def move(self, x: int, y: int, use_max: bool = False) -> bool:
        return self.move_to_xy(self.left + x, y = self.top + y, use_max)

    def move_center(self, x: int, y: int, use_max: bool = False) -> bool:
        x, y = self.xy((x, y))
        return self.move_to_xy(x, y, use_max)

    def __dict__(self) -> Dict:
        return {'top': self.top, 'left': self.left, 'width': int(self.width * self.zoom), 'height': int(self.height * self.zoom)}

class ScreenCapture(StreamInputDevice):

    def __init__(self, monitor: Optional[Monitor] = None, framerate=30):
        self.monitor = monitor or Monitor()
        self.framerate = framerate
        self.frame = None
        self.should_stop = False
        self.is_stopped = True
        self.sct = mss()
        print('Using virtual screen cam...')

    def start(self) -> None:
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        self.is_stopped = False
        return self

    def update(self) -> None:
        while not self.should_stop:
            screenshot = self.sct.grab(self.monitor)
            self.frame = cvtColor(np_array(screenshot), COLOR_RGBA2RGB)
            sleep(1 // self.framerate)
        
        self.is_stopped = True
        self.should_stop = False

    def read(self):
        return self.frame

    def stop(self) -> None:
        self.should_stop = True
        while not self.is_stopped:
            sleep(0.01)

    def set_monitor(self, monitor):
        self.monitor = monitor

    def single_frame(self, monitor: Optional[Monitor] = None):
        with mss() as sct:
            screenshot = sct.grab(monitor or Monitor())
            frame = np_array(screenshot)
            return cvtColor(frame, COLOR_RGBA2RGB)
