import tkinter as tk

class TransparentCaptureWindow:

    def __init__(self, parent, monitor):
        self.parent = parent
        self.monitor = monitor
        self.window = tk.Toplevel(parent)
        self.window.withdraw()  # Hide window initially
        self.window.attributes('-alpha', 0.5)  # Set window transparency
        self.window.overrideredirect(True)  # Remove window decorations
        self.canvas = tk.Canvas(self.window, highlightthickness=0, bg=None)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.update_geometry()
        
        self.canvas.bind('<ButtonPress-1>', self.start_move)
        self.canvas.bind('<ButtonRelease-1>', self.stop_move)
        self.canvas.bind('<B1-Motion>', self.do_move)
        
        self.window.bind('<KeyPress-Up>', lambda e: self.move(0, -1))
        self.window.bind('<KeyPress-Down>', lambda e: self.move(0, 1))
        self.window.bind('<KeyPress-Left>', lambda e: self.move(-1, 0))
        self.window.bind('<KeyPress-Right>', lambda e: self.move(1, 0))
        self.window.bind('<KeyPress-plus>', lambda e: self.zoom(1.1))
        self.window.bind('<KeyPress-minus>', lambda e: self.zoom(0.9))
        
        self.move_x = 0
        self.move_y = 0

    def update_geometry(self):
        self.window.geometry(f'{self.monitor.width}x{self.monitor.height}+{self.monitor.left}+{self.monitor.top}')
        # self.draw_border()

    def draw_border(self):
        self.canvas.delete('all')
        w, h = self.monitor.width, self.monitor.height
        self.canvas.create_rectangle(0, 0, w, h, outline='red', width=10)
        self.canvas.create_rectangle(10, 10, w-10, h-10, outline='red', width=1)

    def start_move(self, event):
        self.move_x = event.x
        self.move_y = event.y

    def stop_move(self, event):
        self.move_x = None
        self.move_y = None
        self.update_monitor()

    def do_move(self, event):
        deltax = event.x - self.move_x
        deltay = event.y - self.move_y
        x = self.window.winfo_x() + deltax
        y = self.window.winfo_y() + deltay
        self.window.geometry(f'+{x}+{y}')

    def move(self, dx, dy):
        x = self.window.winfo_x() + dx
        y = self.window.winfo_y() + dy
        self.window.geometry(f'+{x}+{y}')
        self.update_monitor()

    def zoom(self, factor):
        w = int(self.monitor.width * factor)
        h = int(self.monitor.height * factor)
        self.monitor.width = w
        self.monitor.height = h
        self.update_geometry()
        self.update_monitor()

    def update_monitor(self):
        self.monitor.left = self.window.winfo_x()
        self.monitor.top = self.window.winfo_y()
        self.monitor.width = self.window.winfo_width()
        self.monitor.height = self.window.winfo_height()

    def show(self):
        self.window.deiconify()

    def hide(self):
        self.window.withdraw()

    def toggle(self):
        if self.window.state() == 'withdrawn':
            self.show()
        else:
            self.hide()
