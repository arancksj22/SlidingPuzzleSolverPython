# Installation Instructions

## Tkinter Not Found Error

If you get an error about Tkinter not being available, you have two options:

### Option 1: Install Tkinter (Recommended)

**On macOS with Homebrew:**
```bash
brew install python-tk@3.13
```

Or reinstall Python with Tkinter support:
```bash
brew reinstall python@3.13
```

**On macOS without Homebrew:**
Download and install Python from python.org (includes Tkinter)

**On Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

**On Linux (Fedora):**
```bash
sudo dnf install python3-tkinter
```

### Option 2: Install PyQt5 Alternative

If Tkinter doesn't work, install PyQt5:
```bash
pip3 install PyQt5
```

Then run:
```bash
python3 main_pyqt.py
```

### Option 3: Use Command-Line Version

For a simple command-line demo without GUI:
```bash
python3 demo_cli.py
```

## Running the Application

Once Tkinter is installed:
```bash
python3 main.py
```

Or use the launcher:
```bash
python3 run.py
```

## Quick Test

Test if Tkinter works:
```bash
python3 -c "import tkinter; print('Tkinter is available')"
```

If no error, you're ready to run the application!
