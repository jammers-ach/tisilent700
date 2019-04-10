import logging

from ti700.conn import BrokenSerialIO, InterruptException
from ti700.app import TerminalApp
from apps import all_apps

logger = logging.getLogger(__name__)


class SleepTest(TerminalApp):
    appname = "Sleep test"

    def start(self):
        self.send("sleep test")
        self.sleep(60)
        self.send("seleep over")

class MainTerminal(TerminalApp):


    def start(self):
        self.apps = all_apps()
        while True:
            banner = "TI Slient 700 app"
            leading_spaces = int((self.serial.terminal_width - len(banner)) / 2)
            self.send((" "*leading_spaces) + banner)
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
        for i, app in enumerate(self.apps):
            app_name = app._name()
            self.send("{}) for {}".format(i+1, app_name))

        chosen = None
        while chosen not in range(1, len(self.apps) + 1):
            key = self.read_key("? ")
            try:
                chosen = int(key)
            except ValueError:
                chosen = None
        return self.apps[chosen-1]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-d", "--dummy",
                        action="store_true", dest="dummy", default=False,
                        help="Use stdin/out rather than serial port")

    args = parser.parse_args()

    connection = DummySerial() if args.dummy else BrokenSerialIO()
    tg = MainTerminal(connection)
    tg.start()
