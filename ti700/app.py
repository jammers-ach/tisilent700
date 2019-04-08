import logging
import time

logger = logging.getLogger(__name__)



class TerminalApp():
    '''Base class for a terminal game
    provides send and read mechanims'''

    @classmethod
    def _name(cls):

        return cls.appname if hasattr(cls, 'appname') else "Unnamed application"

    def __init__(self, serial):
        self.serial = serial

    def send(self, text):
        self.serial.send_text(text)

    def print_broken_keys(self):
        '''prints a little helptext for broken keys'''
        if self.serial.brokenkeys == {}:
            # no broken keys
            return
        self.send("This terminal has broken keys: ")
        text = ''
        for i,k in self.serial.brokenkeys.items():
            if k == " ":
                text += "Press '{}' for SPACE, ".format(i)
            else:
                text += "Press '{}' for '{}', ".format(i, k)
        self.send(text)

    def prompt(self, text=""):
        '''Sends a question waits for a response

        game.promt("What is your name? ")
        user then presses types a response and return key
        and this function returns that response
        '''
        self.serial.send_text(text, trailing_newline=False)
        response = self.serial.read_line().lower()
        return response

    def read_key(self, text=""):
        '''Reads a single charater response, without
        wiating for a newline'''
        self.serial.send_text(text, trailing_newline=False)
        response = self.serial.read_char().lower()
        return response

    def start(self):
        raise NotImplemented("Application doesn't have start method")

    def sleep(self, seconds):
        self.serial.sleep(seconds)

