from ti700.app import TerminalApp
from random import randint

class SimpleGame(TerminalApp):
    money = 100
    name = ""

    horses = [
        'Magic horse the fastest horse',
        'Crazy horse the craziest horse',
        'Stupid horse the stupidest horse',
        'Silly horse the one you lease expect',
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
            while key != 'a' and key != 'b':
                key = self.read_key(" ? ").lower()
            self.send("")
            if key == 'b':
                winner = self.race()
            if key == 'a':
                horse, bet = self.get_bet()
                winner = self.race()
                self.money -= bet
                if winner != horse:
                    self.send("Unlucky!!!")
                    self.sleep(1)
                    self.send("You lost ${}".format(bet))
                else:
                    self.send("Congratulations!!!")
                    self.sleep(1)
                    winnings = bet * len(self.horses)
                    self.send("You won ${}".format(winnings))
                    self.money += bet * len(self.horses)

        self.send("Sorry you have no more money :(")
        self.sleep(1)
        self.send("Thank you for playing the simple game")


    def display_money(self):
        self.send("{}, You have ${}".format(self.name, self.money))

    def get_bet(self):
        '''Prompts for the users bet and horse'''
        self.send("Which horse do you want to bet on? ")
        for i, horse in enumerate(self.horses):
            self.send("{}) {}".format(i+1, horse))
        chosen = None
        while chosen not in range(1, len(self.horses) + 1):
            key = self.read_key("? ")
            try:
                chosen = int(key)
            except ValueError:
                chosen = None
        chosen = chosen - 1

        self.send("\nAnd how much do you want to bet on {}?".format(self.horses[chosen]))
        bet = None
        while bet is None:
            read = self.prompt("$")
            try:
                bet = float(read)
            except ValueError:
                bet = Nobne
            if bet and  bet > self.money:
                self.send("{} you only have ${}".format(self.name, self.money))
                bet = None
        return chosen, bet

    def random_horse(self):
        return randint(0, len(self.horses)-1)

    def random_name(self):
        return self.horses[self.random_horse()]

    def race(self):
        short = lambda x: x.split(" ")[0]
        winner = self.random_horse()
        winner_name = self.horses[winner]
        winner_short = short(winner_name)

        random_short = lambda: short(self.random_name())

        self.sleep(2)
        self.send("And they're off")
        self.sleep(1)
        self.send("{} is off to a flying start".format(random_short()))
        self.sleep(3)
        self.send("{} is in a close second".format(random_short()))
        self.sleep(1)
        self.send("{} is still behind".format(random_short()))
        self.sleep(2)
        self.send("But wait.....")
        self.sleep(2)
        self.send("I don't believe this")
        self.sleep(2)
        self.send("{} has just overtaken".format(winner_short))
        self.sleep(2)
        self.send("And the winner is {}".format(winner_name))
        return winner



if __name__ == '__main__':
    from terminalconn import TerminalSerial
    tg = SimpleGame(TerminalSerial())
    tg.get_bet()

