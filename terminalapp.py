import logging

logger = logging.getLogger(__name__)



class TerminalApp():
    '''Base class for a terminal game
    provides send and read mechanims'''


    def __init__(self, serial):
        self.serial = serial

    def send(self, text):
        self.serial.send_text(text)

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


class TestApp(TerminalApp):

    def start(self):
        self.send("I will ask your name, do you a) agree b) disagree?")
        char = ''
        while char != 'a' and char != 'b':
            char = self.read_key("> ")
            self.send("")

        if char == 'a':
            name = self.prompt("\nWhat is your name? ")
            self.send("Hello {}".format(name))
        self.send("Welcome to the game. What is the magic keyword?")

        self.playing = True
        while self.playing:
            response = self.prompt("> ")
            if response == 'test':
                self.playing = False
                self.send("Goodbye")
            else:
                self.send("You said \"{}\" this is wrong".format(response))



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    from terminalconn import TerminalSerial
    tg = TestApp(TerminalSerial())
    tg.start()
