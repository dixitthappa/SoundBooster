from pycaw.pycaw import AudioUtilities

class VolumeController:
    def __init__(self):
        self.device_name = None
        self.volume = None
        self.refresh()

    def refresh(self):
        device = AudioUtilities.GetSpeakers()
        self.device_name = device.FriendlyName
        self.volume = device.EndpointVolume
        return self.volume

    def get_device_name(self):
        self.refresh()
        return self.device_name

    def get_volume(self):
        self.refresh()
        level = self.volume.GetMasterVolumeLevelScalar()
        return round(level * 100)

    def set_volume(self, level: int):
        self.refresh()
        level = max(0, min(100, level))
        self.volume.SetMasterVolumeLevelScalar(level / 100, None)

    def is_muted(self):
        self.refresh()
        return bool(self.volume.GetMute())

    def toggle_mute(self):
        self.refresh()
        current = self.is_muted()
        self.volume.SetMute(not current, None)
