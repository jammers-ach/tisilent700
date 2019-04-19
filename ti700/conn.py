import serial
import io
import sys
import time
import getch
from datetime import datetime

brokenkeys_lookup = {
    ':': ' ',
    ';': 'F',
    '-': 'G'
}

class InterruptException(Exception):
    pass

class BrokenSerialIO(serial.Serial):
    '''A wrapper around the serial io, to handle
    1) remapping broken keys
    2) local echo
    3) reciving \n and sending'''

    def __init__(self, port='/dev/ttyUSB0',
                 baudrate=300,
                 parity=serial.PARITY_EVEN,
                 bytesize=serial.SEVENBITS,
                 stopbits=serial.STOPBITS_ONE,
                 brokenkeys=brokenkeys_lookup):
        super(serial.Serial, self).__init__(port=port,
                           baudrate=baudrate,
                           parity=parity,
                           stopbits=stopbits,
                           bytesize=bytesize)

        self.brokenkeys = brokenkeys_lookup
        self.echo = True
        self.replacenewlines = True

    def _replace(self, char):
        if type(char) is bytes:
            char = char.decode('ascii')

        return self.brokenkeys.get(char, char).encode('ascii')

    def read(self, size=1, **kwargs):
        if self.echo:
            line = []
            for i in range(size):
                c = super(BrokenSerialIO, self).read(size=1, **kwargs)
                if c == b'\r':
                    self.write('\r\n'.encode('ascii'))
                    line.append(b'\n')
                elif c == b'\0':
                    raise InterruptException
                else:
                    c = self._replace(c)
                    self.write(c)
                    line.append(c)

            if size == 1:
                return line[0]
            else:
                return line
        else:
            if size == 1:
                c = super(BrokenSerialIO, self).read(size=1, **kwargs)
                return self._replace(c)
            else:
                chars = super(BrokenSerialIO, self).read(size=size, **kwargs)
                return [self._replace(c) for c in chars.decode('ascii')]


    def write(self, data):
        # replace newlines
        if self.replacenewlines:
            newdata = ""
            for d in data.decode('ascii'):
                if d == '\n':
                    newdata += '\r\n'
                else:
                    newdata += d
            data = newdata.encode('ascii')

        result = super(BrokenSerialIO, self).write(data)
        return result



class DummySerial(io.IOBase):
    '''A class to mimic the size and speed of the
    ti 700'''
    printspeed = 1/30 # 30 characters a second

    def __init__(self):
        self.echo = True
        self.brokenkeys = {}
        # workaround for the serial timeout
        self.timeout = None

    def read(self, size=1):
        if self.timeout:
            time.sleep(self.timeout)
            return

        try:
            if self.echo:
                char = getch.getche()
            else:
                char = getch.getch()
        except KeyboardInterrupt:
            raise InterruptException

        return char.encode('ascii')

    def write(self, data):
        for c in data.decode('ascii'):
            print(c, end="")
            sys.stdout.flush()
            time.sleep(self.printspeed)

