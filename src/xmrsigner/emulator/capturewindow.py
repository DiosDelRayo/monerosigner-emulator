from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt, QPoint

class TransparentCaptureWindow(QWidget):
    def __init__(self, parent, monitor):
        super().__init__(parent, Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.monitor = monitor
        self.setWindowOpacity(0.5)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.update_geometry()
        
        self.move_start = QPoint()
        
    def update_geometry(self):
        self.setGeometry(self.monitor.left, self.monitor.top, self.monitor.width, self.monitor.height)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.red, 10))
        painter.drawRect(self.rect())
        painter.setPen(QPen(Qt.GlobalColor.red, 1))
        painter.drawRect(10, 10, self.width() - 20, self.height() - 20)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.move_start = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.move_start)
            
    def mouseReleaseEvent(self, event):
        self.update_monitor()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.move(self.x(), self.y() - 1)
        elif event.key() == Qt.Key.Key_Down:
            self.move(self.x(), self.y() + 1)
        elif event.key() == Qt.Key.Key_Left:
            self.move(self.x() - 1, self.y())
        elif event.key() == Qt.Key.Key_Right:
            self.move(self.x() + 1, self.y())
        elif event.key() == Qt.Key.Key_Plus:
            self.zoom(1.1)
        elif event.key() == Qt.Key.Key_Minus:
            self.zoom(0.9)
        self.update_monitor()
        
    def zoom(self, factor):
        new_width = int(self.width() * factor)
        new_height = int(self.height() * factor)
        self.resize(new_width, new_height)
        self.monitor.width = new_width
        self.monitor.height = new_height
        
    def update_monitor(self):
        self.monitor.left = self.x()
        self.monitor.top = self.y()
        self.monitor.width = self.width()
        self.monitor.height = self.height()
        
    def show(self):
        super().show()
        
    def hide(self):
        super().hide()
        
    def toggle(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
