from ti700.app import TerminalApp

import io
import subprocess

class TiIO(io.RawIOBase):

    def __init__(self, terminal):
        self.ser = terminal


    def read(self):
        return self.ser.read_char().decode('ascii')

    def write(self, b):
        self.send_text(b.encode('ascii'), trailing_newline=False)

    def fileno(self):
        return 1

class Shell(TerminalApp):
    appname = "shell"

    def start(self):

        self.print_broken_keys()

        io = TiIO(self.serial)

        p = subprocess.Popen('sh', bufsize=0,
                             preexec_fn=os.setsid,
                             stdout=io,
                             stderr=io, shell=True)

        while p.poll() is None:
            pass
