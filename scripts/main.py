from fight import Fight
import random

if __name__ == "__main__":
    fight = Fight()
    fight.simulate()

    for action in fight.get_actions():
        print(action)
