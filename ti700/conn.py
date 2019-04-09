import serial
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

class TerminalSerial():
    '''A class to communicate with the TI slient 700'''

    def __init__(self, port='/dev/ttyUSB0',
                 baudrate=300,
                 parity=serial.PARITY_EVEN,
                 bytesize=serial.SEVENBITS,
                 stopbits=serial.STOPBITS_ONE,
                 brokenkeys=brokenkeys_lookup):

        self.ser = serial.Serial(port=port,
                           baudrate=baudrate,
                           parity=parity,
                           stopbits=stopbits,
                           bytesize=bytesize)

        self.terminal_width = 80

        self.brokenkeys = brokenkeys


    def close(self):
        self.ser.close()

    def __exit__(self):
        self.close()


    def send_text(self, text, trailing_newline=True):
        '''convenient function to wrap a block of text with the
        correct newlines and send it'''
        if trailing_newline and (text == '' or text[-1] != '\n'):
            text += '\n'

        data = text.replace('\n', '\r\n').encode('ascii', 'replace')
        self.ser.write(data)

    def send_line(self):
        '''Prints a horizontal line'''
        line = '=' * self.terminal_width
        self.send_text('\n{}'.format(line))

    def _isnewline(self, char):
        return char == '\r' or char == '\n'

    def is_null(self, data):
        return data == b'\x00'

    def sleep(self, seconds):
        '''Sleeps for a time,

        but will listen for break keys to intterrupt'''

        t1 = datetime.now()
        self.ser.timeout = seconds
        value = self.ser.read()
        self.ser.timeout = None
        t2 = datetime.now()
        elapsed  = (t2 - t1).total_seconds()

        if self.is_null(value):
            raise InterruptException
        else:
            if seconds - elapsed <= 0:
                return
            self.sleep(seconds - elapsed)

    def read_char(self, echo=True):
        '''Reads a single character, echoing back to the serial port
        and translating to sring.

        We expect the serial port to be in half duplex so its our
        responsibility to echo'''
        read_char = self.ser.read(1)

        if self.is_null(read_char):
            raise InterruptException

        read_char = read_char.decode('ascii')
        if self._isnewline(read_char):
            self.ser.write('\r\n'.encode('ascii'))
        else:
            read_char = self.brokenkeys.get(read_char, read_char)
            if echo:
                self.ser.write(read_char.encode('ascii', 'replace'))
        return read_char

    def read_line(self, echo=True):
        '''reads a line of text, echoing back to the serial port
        and translating to sring.

        We expect the serial port to be in half duplex so its our
        responsibility to echo'''
        full_response = ''
        read_char = ''
        while not self._isnewline(read_char):
            read_char = self.read_char(echo)
            if not self._isnewline(read_char):
                full_response += read_char

        return full_response


class DummySerial():
    '''A dummy class for development that prints/reads to standard out'''
    _printspeed = 1/30
    terminal_width = 80
    line_log = 0

    def __init__(self):
        self.brokenkeys = {}
        pass

    def close(self):
        pass

    def __exit__(self):
        pass

    def _slow_print(self, text):
        '''emulates the cool 30 characters a second the ti slient 700 can aparently print at'''
        for c in text:
            print(c, end="")

            if c == '\n':
                self.line_log = 0
            else:
                self.line_log += 1
                if self.line_log > self.terminal_width:
                    print('\n', end="")
                    self.line_log = 0

            sys.stdout.flush()
            time.sleep(self._printspeed)

    def send_text(self, text, trailing_newline=True):
        '''convenient function to wrap a block of text with the
        correct newlines and send it'''
        if trailing_newline and (text == '' or text[-1] != '\n'):
            text += '\n'

        self._slow_print(text)

    def send_line(self):
        '''Prints a horizontal line'''
        line = '=' * self.terminal_width
        self.send_text('\n{}'.format(line))


    def sleep(self, seconds):
        time.sleep(seconds)

    def read_char(self, echo=True):
        return getch.getche()

    def read_line(self, echo=True):
        return input("")
