from ti700.app import TerminalApp
import os
import sys
import select
import termios
import tty
import pty
from subprocess import Popen


class Shell(TerminalApp):
    appname = "unix"
    command = '/bin/sh'

    def start(self):
        self.print_broken_keys()

        master_fd, slave_fd = pty.openpty()
        p = Popen(self.command,
                preexec_fn=os.setsid,
                stdin=slave_fd,
                stdout=slave_fd,
                stderr=slave_fd,
                universal_newlines=True)

        while p.poll() is None:
            r, w, e = select.select([self.serial, master_fd], [], [])
            if sys.stdin in r:
                d = os.read(self.serial.fileno(), 10240)
                os.write(master_fd, d)
            elif master_fd in r:
                o = os.read(master_fd, 10240)
                if o:
                    o = o.decode('utf-8').upper().encode('utf-8')
                    os.write(self.serial.fileno(), o)

