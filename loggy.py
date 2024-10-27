# Modes
MODE_PRESCAN = 0
MODE_ASSEMBLE = 1

# Logging modes
LOG_LEVEL = 1
LOG_ERROR = 0
LOG_WARN = 1
LOG_INFO = 2
LOG_DIAGNOSTIC = 3

def log( level, msg ):
    ind = [ "[!] ", "[?] ", "[+] ", "[@] " ]
    if ( level <= LOG_LEVEL ):
        print ( ind[level] + msg )