import multiprocessing
import os
from slots import LuckyCoin, FruitSlot
from players import Ludoman, Player
import random


class Casino:
    def __init__(self):
        self.all_loses: int = 0
        self.all_wins: int = 0
        self.__balance: int = 10000000
        self.slots: tuple = (LuckyCoin(200), FruitSlot(500))

    def withdrawal(self,lose: int):
        self.__balance -= lose

    def income(self,win: int):
        self.__balance += win

    def all_los_plus(self,x: int):
        self.all_loses += x

    def all_wins_plus(self,x: int):
        self.all_wins += x

    @property
    def balance(self) -> int:
        return self.__balance


class Casino_simulation(Casino):
    def __init__(self, slot=0, number=1000):
        super().__init__()
        self.ludomans = None
        self.slot = self.slots[slot]
        self.numbers = number

    def ludomans_generator(self):
        for _ in range(self.numbers):
            yield Ludoman(random.randint(5000, 60000))

    def start_simulation(self):
        with multiprocessing.Pool(10) as pool:
            for inc, wit in pool.map(self.session, self.ludomans_generator()):
                self.income(inc)
                self.all_los_plus(inc)
                self.withdrawal(wit)
                self.all_wins_plus(wit)

    def session(self, player: Ludoman) -> tuple:
        print(f'{player} starts to play on Slot. {player.status()}')
        income: int = 0
        withdrawal: int = 0
        for _ in range(1000):
            income += self.slot.bet
            player.withdrawal(self.slot.bet)
            money:int  = self.slot.spin()[0] * self.slot.bet
            player.income(money)
            withdrawal += money
            if not player.alive:
                return income,withdrawal
        print(f'{player} stop playing. {player.status()}')
        return income, withdrawal

class Casino_single(Casino):

    def __init__(self, slot=0):
        super().__init__()
        self.options_d = None
        self.player = None
        self.slot = self.slots[slot]

    def start_game(self):
        try:
            self.player = Player(int(input('Enter your balance: ')))
            self.game_loop()
        except ValueError:
            print('Please enter numbers only')
            self.start_game()

    def status(self):
        print(f"Slot: {self.slot}\nCasino balance: {self.balance}\nSlot bet: {self.slot.bet}")

    def change_slot(self):
        print('\n'.join(f"{index + 1}: {i}"for index, i in enumerate(self.slots)))
        self.slot = self.slots[int(input('Choose slot to play: '))-1]

    def spin(self):
        self.player.withdrawal(self.slot.bet)
        if self.player.balance < 0:
            print('Insufficient balance. Please deposit to continue...')
            self.player.income(self.slot.bet)
            return
        self.income(self.slot.bet)
        multiplier, result = self.slot.spin()
        money = multiplier * self.slot.bet
        self.withdrawal(money)
        self.player.income(money)
        print(f'{result}! You win {money}! Your balance {self.player.balance}')

    @staticmethod
    def _exit():
        print('Thanks for playing! Goodbye!')
        input()
        exit()

    def change_bet(self):
        self.slot.change_bet(int(input('How much you want to bet? : ')))

    def print_options(self):
        options: tuple = (
                          ('Spin',self.spin),
                          ('Change bet',self.change_bet),
                          ('Change Slot',self.change_slot),
                          ('Profile', self.player.status), ('Slot info', self.status),
                          ('Exit', self._exit))
        self.options_d: dict = { f"{k}":v for k,v in  zip(range(1,len(options)+1), options)}
        print('\n'.join(f"{index + 1}: {i[0]}" for index, i in enumerate(options)))

    def game_loop(self) -> None:
        os.system('cls')
        print(f'Welcome {self.player} to {self.slot}! Your balance {self.player.balance}.'
              f' Default bet is {self.slot.bet}')
        while self.player.alive:
            self.print_options()
            try:
                self.options_d.get(input('Choose option: '))[1]()
                input()
                os.system('cls')
            except TypeError:
                os.system('cls')
                continue
        return




