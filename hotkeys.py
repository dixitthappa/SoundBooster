import keyboard
from audio import VolumeController

class HotkeyManager:
    def __init__(self, vc: VolumeController):
        self.vc = vc
        self._register()

    def _register(self):
        keyboard.add_hotkey('ctrl+alt+up',    self.volume_up)
        keyboard.add_hotkey('ctrl+alt+down',  self.volume_down)
        keyboard.add_hotkey('ctrl+alt+m',     self.mute_toggle)

    def volume_up(self):
        current = self.vc.get_volume()
        self.vc.set_volume(min(100, current + 5))

    def volume_down(self):
        current = self.vc.get_volume()
        self.vc.set_volume(max(0, current - 5))

    def mute_toggle(self):
        self.vc.toggle_mute()

    def stop(self):
        keyboard.unhook_all_hotkeys()