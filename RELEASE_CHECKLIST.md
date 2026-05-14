# Release Checklist

## Preflight

- Confirm boost starts and stops correctly.
- Confirm **Exit App** stops the boost stream.
- Confirm **Hide to Tray** keeps the app running.
- Confirm Windows output can be returned to real speakers/headphones.
- Confirm VB-Cable is not bundled in the release.
- Update version number in release notes.

## Build

```powershell
powershell -ExecutionPolicy Bypass -File .\build_exe.ps1
```

## Package

Zip this folder:

```text
dist\SoundBooster\
```

Release asset name:

```text
SoundBooster-v0.1.0-beta.zip
```

## Release Notes

```text
SoundBooster v0.1.0 Beta

Initial beta release.

Features:
- Windows volume control
- Mute/unmute
- Tray support
- Global hotkeys
- Virtual-cable boost mode up to 500%
- Live signal meter

Requirements:
- Windows 10/11
- VB-Cable or compatible virtual audio cable for boost mode

Note:
SoundBooster does not include or redistribute VB-Cable.
```
