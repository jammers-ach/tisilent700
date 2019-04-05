import serial

class TerminalSerial():
    '''A class to communicate with the TI slient 700'''

    def __init__(self, port='/dev/ttyUSB0',
                 baudrate=300,
                 parity=serial.PARITY_EVEN,
                 bytesize=serial.SEVENBITS,
                 stopbits=serial.STOPBITS_ONE):

        self.ser = serial.Serial(port=port,
                           baudrate=baudrate,
                           parity=parity,
                           stopbits=stopbits,
                           bytesize=bytesize)


    def close(self):
        self.ser.close()


    def send_text(self, text):
        '''convenient function to wrap a block of text with the
        correct newlines and send it'''
        if text[-1] != '\n':
            text += '\n'

        data = text.replace('\n', '\r\n').encode('ascii', 'replace')

        self.ser.write(data)
