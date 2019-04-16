from ti700.app import TerminalApp

class Reittiopas(TerminalApp):
    appname = "Reittiopas"

    def start(self):
        self.send("Welcome to Reittiopas")

        self.stop = self.prompt("\nPlease enter Stop number? ")


if __name__ == '__main__':
    from terminalconn import TerminalSerial
    ro = Reittiopas(TerminalSerial())

