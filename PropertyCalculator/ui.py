import os

def clearTerminal():
    # Check the OS type to use the appropriate clear command
    if os.name == 'posix':  # Unix/Linux/MacOS
        os.system('clear')
    elif os.name == 'nt':   # Windows
        os.system('cls')