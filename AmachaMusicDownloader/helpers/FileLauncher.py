import subprocess
import os
import sys

def openAFile(filePath):
    """Plays a piece of music with the default music player.
    """
    if sys.platform.startswith("darwin"):
        # macOS
        subprocess.call(("open", filePath))
    elif os.name == "nt":
        # Windows
        os.startfile(filePath)
    elif os.name == "posix":
        # Linux
        subprocess.call(('xdg-open', filePath))