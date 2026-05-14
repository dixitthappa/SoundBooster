# SoundBooster

SoundBooster is a Windows desktop app that can control normal system volume and boost routed audio above 100% using a virtual audio cable.

It is built with Python, PyQt5, pycaw, sounddevice, and numpy.

## Features

- Controls Windows master volume from 0% to 100%.
- Adds mute/unmute controls.
- Runs from the system tray.
- Supports global hotkeys:
  - `Ctrl + Alt + Up` increases volume.
  - `Ctrl + Alt + Down` decreases volume.
  - `Ctrl + Alt + M` toggles mute.
- Boosts routed audio from 100% to 500%.
- Shows live input/output signal levels so users can confirm audio is passing through the booster.

## Important Note About VB-Cable

SoundBooster does not include, install, or redistribute VB-Cable.

Boost mode requires a virtual audio cable installed separately. The app works with compatible virtual audio devices such as VB-Audio Virtual Cable.

Install VB-Cable from the official VB-Audio website:

https://vb-audio.com/Cable/

## Download And Install

1. Go to the GitHub **Releases** page.
2. Download the latest `SoundBooster.zip`.
3. Extract the zip file.
4. Open the extracted folder.
5. Double-click `SoundBooster.exe`.

Keep the full extracted folder together. Do not move only `SoundBooster.exe`, because it needs the `_internal` folder beside it.

## How To Use Normal Volume Control

1. Open `SoundBooster.exe`.
2. Use the top volume slider to control Windows volume.
3. Use **Mute** to mute or unmute system audio.
4. Use **Hide to Tray** if you want the app to keep running in the background.
5. Use **Exit App** when you want to stop the app completely.

## How To Use Boost Mode

First, install VB-Cable or another compatible virtual audio cable.

Then:

1. Open Windows sound output settings.
2. Set Windows output to a virtual cable playback device, such as:

```text
CABLE Input (VB-Audio Virtual Cable)
Speakers (VB-Audio Virtual Cable)
CABLE In 16 Ch (VB-Audio Virtual Cable)
```

3. Open SoundBooster.
4. Set **Input** to:

```text
CABLE Output (VB-Audio Virtual Cable)
```

5. Set **Output** to your real speakers or headphones, for example:

```text
Speakers (Realtek(R) Audio)
Headphones
```

6. Click **Start Boost**.
7. Increase the boost slider slowly.

If the app shows:

```text
Signal: input 0% | output 0%
```

then Windows audio is not reaching SoundBooster yet. Check Windows sound output and Volume Mixer.

## How To Stop Boosted Audio

Click **Exit App** or close the window with the X button. SoundBooster will stop the boost stream before exiting.

Then set Windows sound output back to your real speakers or headphones:

```text
Speakers (Realtek(R) Audio)
Headphones
```

Use **Hide to Tray** only when you want boost mode to keep running in the background.

## Safety

High boost levels can be loud and distorted. Start around 150% or 200%, then increase slowly.

SoundBooster does not record, store, or upload audio. Audio is processed locally on your computer.

## Troubleshooting

**Boost is running but sound is not louder**

Check the signal meter. If input is 0%, Windows audio is not routed to the virtual cable.

**I hear no sound**

Make sure SoundBooster output is set to your real speakers or headphones, not the virtual cable.

**Sound is still boosted after closing**

Make sure you are using the latest version. Click **Exit App**, not **Hide to Tray**. Also set Windows output back to your real speakers/headphones.

**VB-Cable is not listed**

Install VB-Cable from the official VB-Audio website, restart your PC if needed, then click **Refresh Devices** in SoundBooster.

## For Developers

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run from source:

```powershell
python main.py
```

Build the Windows app:

```powershell
powershell -ExecutionPolicy Bypass -File .\build_exe.ps1
```

The packaged app will be created at:

```text
dist\SoundBooster\SoundBooster.exe
```

## Release Package

Release downloads are packaged from:

```text
dist\SoundBooster\
```

Release asset filename format:

```text
SoundBooster-v0.1.0-beta.zip
```

## License

License information will be provided before the first stable release.
