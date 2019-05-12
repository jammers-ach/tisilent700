from ti700.app import TerminalApp
import random
import os
import json
import datetime
import dateutil.parser
import requests

from lunchparser.lounaatinfo import get_menu

import logging
logger = logging.getLogger(__name__)

class LunchReport(TerminalApp):
    appname = "Lunch report"


    def start(self):
        self.send('\n\n')
        day = datetime.date.today()
        self.send("    Lunch report for {}".format(day.isoformat()))
        urls = self.load_urls()

        for url in urls:
            try:
                result = get_menu(url, day)
                self.print_menu(result)
            except Exception as e:
                logger.exception(e)

        self.send("END OF REPORT\n\n\n")


    def print_menu(self, result):
        self.send(result['name'])
        for item in result['food']:
            if type(item) is list:
                item = ', '.join(item)
            self.send(" * {}".format(item))


    def load_urls(self,urlfile='~/.lounaat'):
        fname = os.path.expanduser(urlfile)
        with open(fname) as f:
            result = [a.strip() for a in f.readlines()]
        return result

