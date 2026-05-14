from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from audio import VolumeController
from booster import AudioBooster

STYLE = """
QWidget {
    background-color: #1e1e2e;
    color: #ffffff;
    font-family: Segoe UI;
}
QSlider::groove:horizontal {
    height: 6px;
    background: #3a3a5c;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: #7c6af7;
    width: 18px;
    height: 18px;
    margin: -6px 0;
    border-radius: 9px;
}
QSlider::sub-page:horizontal {
    background: #7c6af7;
    border-radius: 3px;
}
QPushButton {
    background-color: #7c6af7;
    color: white;
    border: none;
    border-radius: 8px;
    min-height: 28px;
    padding: 4px 10px;
    font-size: 13px;
}
QPushButton:hover {
    background-color: #9b8dff;
}
QPushButton:pressed {
    background-color: #5a4fd6;
}
QComboBox {
    background-color: #2a2a44;
    color: white;
    border: 1px solid #3a3a5c;
    border-radius: 6px;
    min-height: 28px;
    padding: 2px 8px;
    font-size: 12px;
}
"""

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.vc = VolumeController()
        self.booster = AudioBooster()
        self.setWindowTitle("Sound Booster")
        self.setMinimumSize(460, 600)
        self.resize(500, 640)
        self.setStyleSheet(STYLE)
        self.init_ui()
        self.start_sync()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(12)

        title = QLabel("🔊 Sound Booster")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.vol_label = QLabel(f"Volume: {self.vc.get_volume()}%")
        self.vol_label.setFont(QFont("Segoe UI", 11))
        self.vol_label.setAlignment(Qt.AlignCenter)
        self.vol_label.setStyleSheet("color: #a0a0c0;")
        layout.addWidget(self.vol_label)

        self.windows_output_label = QLabel(f"Windows output: {self.vc.get_device_name()}")
        self.windows_output_label.setFont(QFont("Segoe UI", 8))
        self.windows_output_label.setAlignment(Qt.AlignCenter)
        self.windows_output_label.setWordWrap(True)
        self.windows_output_label.setStyleSheet("color: #a0a0c0;")
        layout.addWidget(self.windows_output_label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(self.vc.get_volume())
        self.slider.valueChanged.connect(self.on_slider_change)
        layout.addWidget(self.slider)

        self.mute_btn = QPushButton("Mute")
        self.mute_btn.setFont(QFont("Segoe UI", 10))
        self.mute_btn.clicked.connect(self.on_mute_toggle)
        layout.addWidget(self.mute_btn)

        route_label = QLabel("Boost route")
        route_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        route_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(route_label)

        self.input_combo = QComboBox()
        self.output_combo = QComboBox()
        self.input_combo.setMinimumHeight(32)
        self.output_combo.setMinimumHeight(32)
        self.load_audio_devices()
        layout.addWidget(self.input_combo)
        layout.addWidget(self.output_combo)

        self.refresh_btn = QPushButton("Refresh Devices")
        self.refresh_btn.setFont(QFont("Segoe UI", 10))
        self.refresh_btn.clicked.connect(self.load_audio_devices)
        layout.addWidget(self.refresh_btn)

        self.boost_label = QLabel("Boost: 100%")
        self.boost_label.setFont(QFont("Segoe UI", 11))
        self.boost_label.setAlignment(Qt.AlignCenter)
        self.boost_label.setStyleSheet("color: #a0a0c0;")
        layout.addWidget(self.boost_label)

        self.boost_slider = QSlider(Qt.Horizontal)
        self.boost_slider.setMinimum(100)
        self.boost_slider.setMaximum(500)
        self.boost_slider.setSingleStep(10)
        self.boost_slider.setPageStep(25)
        self.boost_slider.setValue(100)
        self.boost_slider.valueChanged.connect(self.on_boost_change)
        layout.addWidget(self.boost_slider)

        self.boost_btn = QPushButton("Start Boost")
        self.boost_btn.setFont(QFont("Segoe UI", 10))
        self.boost_btn.clicked.connect(self.on_boost_toggle)
        layout.addWidget(self.boost_btn)

        self.level_label = QLabel("Signal: input 0% | output 0%")
        self.level_label.setFont(QFont("Segoe UI", 9))
        self.level_label.setAlignment(Qt.AlignCenter)
        self.level_label.setStyleSheet("color: #a0a0c0;")
        layout.addWidget(self.level_label)

        self.status_label = QLabel("Route Windows output to VB-Cable, then start boost.")
        self.status_label.setFont(QFont("Segoe UI", 9))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.setMinimumHeight(44)
        self.status_label.setStyleSheet("color: #a0a0c0;")
        layout.addWidget(self.status_label)

        app_controls = QHBoxLayout()
        app_controls.setSpacing(10)

        self.hide_btn = QPushButton("Hide to Tray")
        self.hide_btn.setFont(QFont("Segoe UI", 10))
        self.hide_btn.clicked.connect(self.hide_to_tray)
        app_controls.addWidget(self.hide_btn)

        self.exit_btn = QPushButton("Exit App")
        self.exit_btn.setFont(QFont("Segoe UI", 10))
        self.exit_btn.clicked.connect(self.exit_app)
        self.exit_btn.setStyleSheet("background-color: #d84f68;")
        app_controls.addWidget(self.exit_btn)

        layout.addLayout(app_controls)

        self.setLayout(layout)

    def load_audio_devices(self):
        self.input_combo.clear()
        self.output_combo.clear()

        for device in self.booster.list_input_devices():
            label = f"Input: {device['name']} [{device['hostapi']}]"
            self.input_combo.addItem(label, (device["hostapi"], device["name"]))
            self.input_combo.setItemData(self.input_combo.count() - 1, label, Qt.ToolTipRole)

        for device in self.booster.list_output_devices():
            label = f"Output: {device['name']} [{device['hostapi']}]"
            self.output_combo.addItem(label, (device["hostapi"], device["name"]))
            self.output_combo.setItemData(self.output_combo.count() - 1, label, Qt.ToolTipRole)

        self.select_device(self.input_combo, self.booster.pick_default_input())
        self.select_device(self.output_combo, self.booster.pick_default_output())

    def select_device(self, combo, device_index):
        index = combo.findData(device_index)
        if index >= 0:
            combo.setCurrentIndex(index)

    def on_slider_change(self, value):
        self.vc.set_volume(value)
        self.booster.set_output_volume(value)
        self.booster.set_output_muted(value <= 0)
        self.vol_label.setText(f"Volume: {value}%")

    def on_mute_toggle(self):
        self.vc.toggle_mute()
        muted = self.vc.is_muted()
        self.booster.set_output_muted(muted)
        self.mute_btn.setText("Unmute" if muted else "Mute")

    def on_boost_change(self, value):
        self.booster.set_boost(value)
        self.boost_label.setText(f"Boost: {value}%")

    def on_boost_toggle(self):
        if self.booster.is_running():
            self.stop_booster()
            return

        input_device = self.input_combo.currentData()
        output_device = self.output_combo.currentData()

        try:
            self.booster.set_output_volume(self.vc.get_volume())
            self.booster.set_output_muted(self.vc.is_muted())
            self.booster.start(input_device, output_device)
        except Exception as exc:
            QMessageBox.warning(self, "Boost failed", str(exc))
            self.status_label.setText("Boost failed. Check VB-Cable and selected devices.")
            return

        self.boost_btn.setText("Stop Boost")
        self.status_label.setText("Boost is running.")

    def stop_booster(self):
        self.booster.stop()
        self.boost_btn.setText("Start Boost")
        self.status_label.setText("Boost stopped.")
        self.level_label.setText("Signal: input 0% | output 0%")

    def hide_to_tray(self):
        self.hide()

    def exit_app(self):
        self.stop_booster()
        app = QApplication.instance()
        if app:
            app.quit()

    def start_sync(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.sync_volume)
        self.timer.start(500)

    def sync_volume(self):
        vol = self.vc.get_volume()
        self.slider.blockSignals(True)
        self.slider.setValue(vol)
        self.slider.blockSignals(False)
        self.booster.set_output_volume(vol)
        self.vol_label.setText(f"Volume: {vol}%")
        self.windows_output_label.setText(f"Windows output: {self.vc.get_device_name()}")
        muted = self.vc.is_muted()
        self.booster.set_output_muted(muted or vol <= 0)
        self.mute_btn.setText("Unmute" if muted else "Mute")
        self.sync_booster_levels()

    def sync_booster_levels(self):
        if not self.booster.is_running():
            return

        input_level, output_level = self.booster.get_levels()
        self.level_label.setText(f"Signal: input {input_level}% | output {output_level}%")
        if input_level <= 1:
            self.status_label.setText("Boost is running, but no VB-Cable input signal is detected.")
        else:
            self.status_label.setText("Boost is running.")

    def closeEvent(self, event):
        self.exit_app()
        event.accept()
