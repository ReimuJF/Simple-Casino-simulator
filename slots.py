import random


class LuckyCoin:
    __WEIGHT: list = [0.15, 0.17, 0.14, 0.13, 0.14, 0.14, 0.15, 0.10, 0.09, 0.09]
    __MULTIPLIER_D: dict = { "777": 500, "999": 250, "333": 50,
                             "888": 25, "555": 25, "444": 20, "222": 15, "111": 10 }


    def __init__(self, bet: int):
        self.bet  = bet

    def generate_number(self) -> str:
        return f"{''.join(str(i) for i in random.choices(range(10), weights=self.__WEIGHT, k=3)):>03}"

    def spin(self) -> tuple:
        point: str = self.generate_number()
        multiplier:int = 0

        if point in self.__MULTIPLIER_D:
            multiplier = self.__MULTIPLIER_D[point]
        elif point[0] == point[1] and point[0] in {'9','8','7','5'}:
            multiplier = 5
        elif point[0] == point[1] and point[0] in {'4','3','2','1'}:
            multiplier = 3
        elif point[0] == '7':
            multiplier = 2
        elif point[0] == '1':
            multiplier = 1
        return multiplier,point

    def change_bet(self,bet):
        if bet > 250000:
            print('Bet too high! Maximum is 250000')
        else:
            self.bet = bet

    def __repr__(self):
        return self.__class__.__name__


class FruitSlot(LuckyCoin):
    __WEIGHT: list = [14, 15, 17, 17, 17, 20, 20, 25, 25, 27]
    __FRUITS: dict = {"Wild": 10, "Star": 9, "Bell": 8, "Shell": 7, "Seven": 6,
                "Cherry": 5, "Bar": 4, "King": 3, "Queen": 2, "Jack": 1}

    def generate_result(self) -> list:
        return random.choices(list(self.__FRUITS.keys()), weights=self.__WEIGHT, k=3)

    def spin(self, option='single') -> tuple:
        result: list = self.generate_result()
        multiplier: int = 0
        if result[0] == result[1] == result[2]:
            multiplier = 10 * self.__FRUITS[result[0]]
        elif result[0] == result[2] == 'Wild':
            multiplier = self.__FRUITS[result[0]]
        elif (result[0] == result[2] and result[1] == 'Wild') or (result[0] == result[1] and result[2] == 'Wild'):
            multiplier = 2 * self.__FRUITS[result[0]]
        elif result[0] == result[1]:
            multiplier = self.__FRUITS[result[0]]
        return {'single': (multiplier,result), 'simulation': multiplier}[option]

