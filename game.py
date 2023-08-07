from casino import Casino_simulation, Casino_single
import time

def simulation():
    start = time.perf_counter()
    cas = Casino_simulation(slot=1, number=1500) # 0 LuckyCoin, 1 FruitSpin, number is number of players
    cas.start_simulation()
    end = time.perf_counter()

    print(f'After {cas.numbers} players, casino balance change to {cas.balance}. ')
    print(f'wins {cas.all_wins} loses {cas.all_loses} {(cas.all_wins / cas.all_loses):.2%}')
    print(f'Time spent {time.strftime("%H:%M:%S",time.gmtime(end - start))}')

def single():
    casinich = Casino_single(1)
    casinich.start_game()


if __name__ == "__main__":
    options: tuple = (("Simulation", simulation), ("Single Player", single))
    print('\n'.join(f"{index}: {v[0]}" for index, v in enumerate(options, 1)))
    try:
        options[int(input("Choose option: "))-1][1]()
    except ValueError:
        exit()
    finally:
        print('Thanks for playing! Goodbye!')
