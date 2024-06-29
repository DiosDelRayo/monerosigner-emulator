from PyQt6.QtWidgets import QApplication
from sys import exit, argv


app = QApplication(argv)


from xmrsigner.controller import Controller
from xmrsigner.emulator.desktopDisplay import DesktopDisplay

# Get the one and only Controller instance and start our main loop
Controller.get_instance().start()
desktop_display = DesktopDisplay()
desktop_display.show()
sys.exit(app.exec_())
