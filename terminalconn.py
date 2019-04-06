import serial

brokenkeys_lookup = {
    ':': ' ',
    ';': 'F',
    '-': 'G'
}

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

        self.terminal_width = 30

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

    def read_char(self, echo=True):
        '''Reads a single character, echoing back to the serial port
        and translating to sring.

        We expect the serial port to be in half duplex so its our
        responsibility to echo'''
        read_char = self.ser.read(1).decode('ascii')
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
