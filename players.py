import random
from itertools import count


class Ludoman:
    _ids = count(1)
    def __init__(self, balance: int):
        self._id: int = next(self._ids)
        self.balance: int = balance
        self.debt: int = 0
        self.sanity: int = random.randint(1,5)
        self.alive: bool = True

    def withdrawal(self, lose: int):
        self.balance -= lose
        if self.balance < 0:
            self.dodep(random.randint(20000,60000))

    def income(self, win: int):
        self.balance += win
        if win >= 50000:
            self.__winner()

    def dodep(self, dep: int):
        self.sanity -= 1
        if self.sanity < 0:
            self.__suicide()
        self.balance += dep
        self.debt += dep

    def status(self) -> str:
        return f"Balance: {self.balance} Debt: {self.debt} Sanity: {self.sanity}"

    def __suicide(self):
        print(f'{self} decide to leave... His debt {self.debt}.')
        self.alive = False

    def __winner(self):
        print(f'{self} win big prize and stop playing. {self.status()} #Bigwin!')
        self.alive = False

    def __repr__(self) -> str:
        return f'Ludoman {self._id:0>5}'

class Player(Ludoman):

    def withdrawal(self, lose: int):
        self.balance -= lose
        if self.balance <= 0:
            try:
                self.dodep(int(input('How much you want to deposit? ')))
            except ValueError:
                print('Please enter numbers only')

    def dodep(self, dep: int):
        if dep > 0:
            self.sanity -= 1
        if self.sanity < 0:
            self.__suicide()
        self.balance += dep
        self.debt += dep

    def status(self):
        print(f"{self}\nBalance: {self.balance}\nDebt: {self.debt}\nSanity: {self.sanity}")

    def __suicide(self):
        print(f'You cant deposit anymore your debt {self.debt}')
        self.alive = False

    def income(self, win: int):
        self.balance += win

    def __repr__(self) -> str:
        return f'Player {str(id(self))[-6:]}'