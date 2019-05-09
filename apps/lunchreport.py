from ti700.app import TerminalApp
import random
import json
import datetime
import dateutil.parser
import requests

class LunchReport(TerminalApp):
    appname = "Lunch report"

    amica_urls = [
        "https://www.amica.fi/modules/json/json/Index?costNumber=3008&language=fi",
    ]

    def start(self):
        self.send('\n\n')
        day = datetime.date.today()
        self.send("    Lunch report for {}".format(day.isoformat()))

        for url in self.amica_urls:
            result = self.get_and_parse_amica(url, day)
            self.print_menu(result)

        self.send("END OF REPORT\n\n\n")


    def get_and_parse_amica(self, url, ourday):
        resp = requests.get(url)
        data = resp.json()
        food = []
        location = data['RestaurantName']
        for day in data['MenusForDays']:
            date = dateutil.parser.parse(day['Date']).date()
            if date == ourday:
                for menu in day['SetMenus']:
                    food.append(menu['Components'])

        return {
            'name': location,
            'food': food
        }


    def print_menu(self, result):
        self.send(result['name'])
        for item in result['food']:
            if type(item) is list:
                item = ', '.join(item)
            self.send(" * {}".format(item))
