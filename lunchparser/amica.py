import datetime
import dateutil.parser
import requests

def get_and_parse_amica(url, ourday):
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
