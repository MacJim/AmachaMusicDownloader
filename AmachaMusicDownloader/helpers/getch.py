import sys

def getch():
    """Get a single character from user input. The user is not required to press ENTER.

    Source (many thanks): https://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user
    """
    try:
        # Only works on Windows.
        import msvcrt
        return msvcrt.getch()

    except ModuleNotFoundError:
        # Works on UNIX.
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def pressAnyKeyToContinue():
    print("Press any key to continue...", end = "")
    sys.stdout.flush()
    getch()