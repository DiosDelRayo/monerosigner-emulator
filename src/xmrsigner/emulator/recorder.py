from PIL import Image
from time import time
from typing import Optional, List, Tuple
from pathlib import Path


class ScreenRecorder:

    def __init__(self, filename: str):
        self.recording = False
        self.frames: List[Tuple[Image, int]] = []
        self.last_frame: Optional[Image] = None
        self.last_frame_time: Optional[int] = None
        self.output_filename = filename

    def record(self) -> None:
        self.recording = True

    def stop(self) -> None:
        if not self.recording:
            return
        self.recording = False
        if len(self.frames) > 0:
            self.save_gif()

    def record_frame(self, frame: Image) -> None:
        if not self.recording:
            return

        if self.last_frame is None:
            self.add_frame(frame, 0)
            return
        if self.is_same_frame(frame):
            return # drop frame, nothing changed
        self.add_frame(frame, int((time() - self.last_frame_time) * 1000))  # Convert to milliseconds

    def add_frame(self, frame: Image, duration: int) -> None:
        self.frames.append((frame.copy(), duration))
        self.last_frame = frame.copy()
        self.last_frame_time = time()

    def is_same_frame(self, frame: Image) -> bool:
        return frame is not None and list(frame.getdata()) == list(self.last_frame.getdata())

    def save_gif(self) -> None:
        if not self.frames or len(self.frames) == 0:
            return

        duration: float = time() - self.last_frame_time
        first_frame, _ = self.frames[0]
        filename = Path(self.output_filename.replace('{{ timestamp }}', str(int(time())))).absolute()
        first_frame.save(
            filename,
            save_all=True,
            append_images=[frame for frame, _ in self.frames[1:]],
            duration=[duration for _, duration in self.frames],
            loop=0
        )
        print(f"Screen recording saved as {filename} with a duration of {int(duration)} seconds.")
