.\venv\Scripts\python.exe -m PyInstaller `
    --noconfirm `
    --clean `
    --windowed `
    --name SoundBooster `
    --icon assets\icon.ico `
    "--add-data=assets:assets" `
    main.py
