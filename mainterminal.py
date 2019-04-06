import logging

from terminalconn import TerminalSerial, DummySerial, InterruptException
from terminalapp import TerminalApp
from simplegame import SimpleGame
from terminalemail import EmailApp

logger = logging.getLogger(__name__)


class SleepTest(TerminalApp):

    def start(self):
        self.send("sleep test")
        self.sleep(60)
        self.send("seleep over")

class MainTerminal(TerminalApp):

    apps = [
        ('sleep test', SleepTest),
        ('a game', SimpleGame),
        ('email checker', EmailApp),
    ]
    def start(self):
        while True:
            self.send("TI Slient 700 app")
            self.print_broken_keys()

            try:
                app = self.prompt_applist()
            except InterruptException:
                pass

            try:
                a = app(self.serial)
                a.start()
            except InterruptException:
                self.send("\n\nExit\n")



    def prompt_applist(self):
        '''Prompts the user for the chosen app,
        returns the class of the app they chose'''
        for i, p in enumerate(self.apps):
            app_name, _ = p
            self.send("{}) for {}".format(i+1, app_name))

        chosen = None
        while chosen not in range(1, len(self.apps) + 1):
            key = self.read_key("? ")
            try:
                chosen = int(key)
            except ValueError:
                chosen = None
        return self.apps[chosen-1][1]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-d", "--dummy",
                        action="store_true", dest="dummy", default=False,
                        help="Use stdin/out rather than serial port")

    args = parser.parse_args()
    connection = DummySerial() if args.dummy < 2 else TerminalSerial()
    tg = MainTerminal(connection)
    tg.start()
