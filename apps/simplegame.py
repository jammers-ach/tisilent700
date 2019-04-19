from ti700.app import TerminalApp
import random
import json

class SimpleGame(TerminalApp):
    money = 100
    appname = "a simple game"
    name = ""

    horses = [
        'Magic horse',
        'Crazy horse',
        'Stupid horse',
        'Silly horse',
        'Wonder horse',
        'Foxy horse',
        'Triuphant horse'
    ]

    wins = {}
    house_balance = 0
    wins_file = '.horse_data'

    def start(self):
        self.load_wins()
        self.send("Welcome to the Horse races")

        self.name = self.prompt("\nWhat is your name? ")
        self.sleep(1)

        self.play()


    def load_wins(self):
        try:
            with open(self.wins_file) as f:
                data = json.load(f)
                self.wins = data.get('wins', {})
                self.house_balance = data.get('balance', 0)
        except FileNotFoundError:
            return

    def save_wins(self):
        with open(self.wins_file, 'w') as f:
            json.dump({'wins':self.wins,
                       'balance': self.house_balance}, f)



    def play(self):
        while self.money > 0:
            self.display_money()
            key = None
            self.send("New race!!!")
            self.send("a) place a bet, b) watch race")
            horse_list = self.generate_list()
            while key != 'a' and key != 'b':
                key = self.read_key(" ? ").lower()
            self.send("")
            if key == 'b':
                winner = self.race(horse_list)
            if key == 'a':
                horse, bet = self.get_bet(horse_list)
                self.house_balance += bet
                self.money -= bet
                winner = self.race(horse_list)
                if winner != horse:
                    self.send("Unlucky!!! ", trailing_newline=False)
                    self.sleep(1)
                    self.send("You lost ${}".format(bet))
                else:
                    self.send("Congratulations!!! ", trailing_newline=False)
                    self.sleep(1)
                    winnings = bet * len(horse_list)
                    self.send("You won ${}".format(winnings))
                    self.money += winnings
                    self.house_balance -= bet
                self.save_wins()

        self.send("Sorry you have no more money :(")
        self.sleep(1)
        self.send("Thank you for playing the simple game")

    def generate_list(self, num_horses=4):
        '''Generates a list of which horses will play'''
        return random.sample(self.horses, num_horses)

    def display_money(self):
        self.send("{}, You have ${}".format(self.name, self.money))

    def get_bet(self, horse_list):
        '''Prompts for the users bet and horse'''
        self.send("Which horse do you want to bet on? ")
        index = self.multiple_choices(["{} - {} wins".format(horse, self.wins.get(horse, 0)) for horse in horse_list])
        chosen = horse_list[index]

        self.send("\nAnd how much do you want to bet on {}?".format(chosen))
        bet = None
        while bet is None:
            read = self.prompt("$")
            try:
                bet = float(read)
            except ValueError:
                bet = None
            if bet and  bet > self.money:
                self.send("{} you only have ${}".format(self.name, self.money))
                bet = None
        return chosen, bet



    def race(self, horse_list):
        short = lambda x: x.split(" ")[0]
        short_horse = lambda x: short(horse_list[x])
        random.shuffle(horse_list)
        winner = horse_list[0]

        assert len(horse_list) >= 4

        order = [0, 1, 2, 3]
        random.shuffle(order)

        self.sleep(2)
        self.send("And they're off. ", trailing_newline=False)
        self.sleep(1)
        self.send("{} is off to a flying start. ".format(short_horse(order[0])), trailing_newline=False)
        self.sleep(2)
        self.send("{} is in a close second. ".format(short_horse(order[1])))
        self.sleep(3)
        self.send("{} is still behind. ".format(short_horse(order[2])), trailing_newline=False)
        self.sleep(2)
        self.send("{} is catching up".format(short_horse(order[3])))
        self.sleep(2)
        self.send("But wait..... ", trailing_newline=False)
        self.sleep(2)
        self.send("I don't believe this. ", trailing_newline=False)

        if horse_list[order[0]] == winner:
            self.sleep(2)
            self.send("{} has just overtaken. ".format(short_horse(order[2])), trailing_newline=False)
            self.sleep(1)
            self.send("but is falling behind")
        else:
            self.sleep(2)
            self.send("{} has just overtaken".format(short(winner)))

        self.sleep(2)
        self.send("And the winner is {}".format(winner))

        if winner not in self.wins:
            self.wins[winner] = 1
        else:
            self.wins[winner] += 1

        self.save_wins()
        return winner



if __name__ == '__main__':
    from terminalconn import TerminalSerial
    tg = SimpleGame(TerminalSerial())
    tg.get_bet()

