# PYCRPG

A turn-based card game developed in python.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/chenglyes/pycrpg.git
cd pycrpg
```

### 2. Create a virtual environment (Recommended)
- venv、anaconda...

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### Development Mode
```bash
python launch.py
```

### Build Executable (Windows)
```bash
# Install PyInstaller if not already installed
pip install pyinstaller

# Build the executable
pyinstaller launch.py --name pycrpg --add-data "data:data" --windowed

# For a single file executable
pyinstaller launch.py --name pycrpg --add-data "data:data" --windowed --onefile
```

The executable will be created in the `dist` folder.

## Project Structure

```
project/
├── scripts/            # Source code
├── tests/              # Test code
├── data/               # Data files and resources
├── dist/               # Built executables (after build)
├── requirements.txt    # Python dependencies
└── launch.py           # Main entry point
```

## Support

For issues and questions:
1. Open an issue on GitHub
2. Contact me
