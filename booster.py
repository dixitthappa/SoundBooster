import numpy as np
import sounddevice as sd


class BoosterError(RuntimeError):
    pass


class AudioBooster:
    HOST_PRIORITY = ("Windows DirectSound", "MME", "Windows WASAPI", "Windows WDM-KS")

    def __init__(self):
        self.boost_percent = 100
        self.output_volume_percent = 100
        self.output_muted = False
        self.input_device = None
        self.output_device = None
        self.stream = None
        self.input_level = 0
        self.output_level = 0

    def list_input_devices(self):
        return self._devices("input")

    def list_output_devices(self):
        return self._devices("output")

    def set_boost(self, percent: int):
        self.boost_percent = max(100, min(500, int(percent)))

    def set_output_volume(self, percent: int):
        self.output_volume_percent = max(0, min(100, int(percent)))

    def set_output_muted(self, muted: bool):
        self.output_muted = bool(muted)

    def start(self, input_device=None, output_device=None):
        if self.stream:
            return

        input_device = self.resolve_device(input_device, "input")
        output_device = self.resolve_device(output_device, "output")
        self.input_device = input_device
        self.output_device = output_device
        in_info = sd.query_devices(input_device, "input")
        out_info = sd.query_devices(output_device, "output")

        channels = min(
            int(in_info.get("max_input_channels", 0)),
            int(out_info.get("max_output_channels", 0)),
            2,
        )
        if channels <= 0:
            raise BoosterError("Selected devices do not support audio routing.")

        samplerate = int(out_info.get("default_samplerate") or in_info.get("default_samplerate") or 48000)

        self.stream = sd.Stream(
            device=(input_device, output_device),
            samplerate=samplerate,
            channels=channels,
            dtype="float32",
            blocksize=1024,
            latency="low",
            callback=self._callback,
        )
        self.stream.start()

    def stop(self):
        if not self.stream:
            return

        self.stream.stop()
        self.stream.close()
        self.stream = None

    def is_running(self):
        return self.stream is not None

    def get_levels(self):
        return self.input_level, self.output_level

    def pick_default_input(self):
        devices = self.list_input_devices()
        cable = self._find_device(devices, ("cable output", "vb-audio", "vb-cable"))
        return cable if cable is not None else sd.default.device[0]

    def pick_default_output(self):
        devices = self.list_output_devices()
        physical_devices = [
            device for device in devices
            if not self._matches(device, ("vb-audio", "vb-cable", "cable"))
        ]
        speaker = self._find_device(physical_devices, ("speaker", "headphone", "realtek"))
        return speaker if speaker is not None else sd.default.device[1]

    def resolve_device(self, identity, kind):
        if isinstance(identity, int):
            return identity

        if isinstance(identity, tuple) and len(identity) == 2:
            hostapi_name, device_name = identity
            for device in self._devices(kind):
                if device["hostapi"] == hostapi_name and device["name"] == device_name:
                    return device["index"]

        return identity

    def _callback(self, indata, outdata, frames, time, status):
        if self.output_muted or self.output_volume_percent <= 0:
            outdata.fill(0)
            self.input_level = self._level_percent(indata)
            self.output_level = 0
            return

        gain = (self.boost_percent / 100.0) * (self.output_volume_percent / 100.0)
        boosted = indata * gain

        # Soft clipping keeps 500% from becoming hard digital crackle immediately.
        outdata[:] = np.tanh(boosted).astype(np.float32)
        self.input_level = self._level_percent(indata)
        self.output_level = self._level_percent(outdata)

    def _devices(self, kind):
        devices = []
        hostapis = sd.query_hostapis()
        for index, device in enumerate(sd.query_devices()):
            max_channels = device.get(f"max_{kind}_channels", 0)
            if max_channels > 0:
                hostapi = hostapis[device["hostapi"]]["name"]
                devices.append(
                    {
                        "index": index,
                        "name": device["name"],
                        "hostapi": hostapi,
                        "channels": int(max_channels),
                    }
                )
        return sorted(devices, key=self._sort_key)

    def _find_device(self, devices, terms):
        for device in devices:
            if self._matches(device, terms):
                return (device["hostapi"], device["name"])
        return None

    def _matches(self, device, terms):
        name = device["name"].lower()
        return any(term in name for term in terms)

    def _sort_key(self, device):
        try:
            host_rank = self.HOST_PRIORITY.index(device["hostapi"])
        except ValueError:
            host_rank = len(self.HOST_PRIORITY)

        return (host_rank, device["name"].lower())

    def _level_percent(self, samples):
        if samples.size == 0:
            return 0

        peak = float(np.max(np.abs(samples)))
        return max(0, min(100, int(round(peak * 100))))
