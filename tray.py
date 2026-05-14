import pystray
from PIL import Image
from PyQt5.QtCore import QObject, pyqtSignal
from paths import resource_path

class TrayIcon(QObject):
    show_window = pyqtSignal()
    quit_app = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.icon = self._build_icon()

    def _build_icon(self):
        image = Image.open(resource_path("assets/icon.png"))
        menu = pystray.Menu(
            pystray.MenuItem("Open", self._on_open, default=True),
            pystray.MenuItem("Quit", self._on_quit)
        )
        return pystray.Icon("SoundBooster", image, "Sound Booster", menu)

    def _on_open(self, icon, item):
        self.show_window.emit()

    def _on_quit(self, icon, item):
        self.icon.stop()
        self.quit_app.emit()

    def run(self):
        self.icon.run_detached()

    def stop(self):
        self.icon.stop()
