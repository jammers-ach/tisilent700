import logging
import serial

from ti700.conn import BrokenSerialIO, DummySerial, InterruptException
from ti700.app import TerminalApp

from apps import all_apps

logger = logging.getLogger(__name__)


class MainTerminal(TerminalApp):

    def start(self):
        self.apps = all_apps()
        try:
            self.runmenu()
        except InterruptException:
            logger.info("Terminal shut down or exited")

    def runmenu(self):
        while True:
            logger.info("Starting app")

            # When the terminal first starts, it sends null
            # So we should wait for that if we're a real terminal
            if (isinstance(self.serial, BrokenSerialIO)):
                logger.info("waiting for terminal switch on")
                try:
                    self.read_key("")
                except InterruptException:
                    pass


            banner = "TI Slient 700 app"
            leading_spaces = int((self.terminal_width - len(banner)) / 4)
            self.send((" "*leading_spaces) + banner)
            self.print_broken_keys()

            app = self.prompt_applist()

            a = app(self.serial)
            logger.info("They chose %s", app.__class__)
            a.start()



    def prompt_applist(self):
        '''Prompts the user for the chosen app,
        returns the class of the app they chose'''
        chosen = self.multiple_choices([app._name() for app in self.apps])
        return self.apps[chosen]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-d", "--dummy",
                        action="store_true", dest="dummy", default=False,
                        help="Use stdin/out rather than serial port")

    args = parser.parse_args()

    if not args.dummy:
        logging.basicConfig(level=logging.DEBUG)


    connection = DummySerial() if args.dummy else BrokenSerialIO()
    tg = MainTerminal(connection)
    tg.start()
