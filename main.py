import sys
from PyQt5.QtWidgets import QApplication
from ui import MainWindow
from tray import TrayIcon
from hotkeys import HotkeyManager

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

window = MainWindow()
window.show()

tray = TrayIcon()
tray.show_window.connect(window.show)
tray.quit_app.connect(app.quit)
tray.run()

hotkeys = HotkeyManager(window.vc)

def cleanup():
    window.stop_booster()
    hotkeys.stop()
    tray.stop()

app.aboutToQuit.connect(cleanup)

sys.exit(app.exec())
