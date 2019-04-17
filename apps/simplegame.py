from ti700.app import TerminalApp
import random

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

    def start(self):
        self.send("Welcome to the Horse races")

        self.name = self.prompt("\nWhat is your name? ")
        self.sleep(1)

        self.play()

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
                winner = self.race(horse_list)
                self.money -= bet
                if winner != horse:
                    self.send("Unlucky!!!")
                    self.sleep(1)
                    self.send("You lost ${}".format(bet))
                else:
                    self.send("Congratulations!!!")
                    self.sleep(1)
                    winnings = bet * len(horse_list)
                    self.send("You won ${}".format(winnings))
                    self.money += bet * len(winnings)

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
        for i, horse in enumerate(horse_list):
            self.send("{}) {}".format(i+1, horse))
        chosen = None
        while chosen not in range(1, len(horse_list) + 1):
            key = self.read_key("? ")
            try:
                chosen = int(key)
            except ValueError:
                chosen = None
        chosen = horse_list[chosen - 1]

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
        self.send("And they're off")
        self.sleep(1)
        self.send("{} is off to a flying start".format(short_horse(order[0])))
        self.sleep(1)
        self.send("{} is in a close second".format(short_horse(order[1])))
        self.sleep(1)
        self.send("{} is still behind".format(short_horse(order[2])))
        self.sleep(1)
        self.send("{} is catching up".format(short_horse(order[3])))
        self.sleep(2)
        self.send("But wait.....")
        self.sleep(2)
        self.send("I don't believe this")

        if order[0] == winner:
            self.sleep(2)
            self.send("{} has just overtaken".format(short(order[2])))
            self.sleep(1)
            self.send("but is falling behind")
        else:
            self.sleep(2)
            self.send("{} has just overtaken".format(short(winner)))

        self.sleep(2)
        self.send("And the winner is {}".format(winner))
        return winner



if __name__ == '__main__':
    from terminalconn import TerminalSerial
    tg = SimpleGame(TerminalSerial())
    tg.get_bet()

