import random

while True:
    level = input("Level: ")

    if level.isdigit() and int(level) > 0:
        level = int(level)
        break

number = random.randint(1, level)

while True:
    guess = input("Guess: ")

    if not guess.isdigit():
        continue

    guess = int(guess)

    if guess < number:
        print("Too small!")
    elif guess > number:
        print("Too large!")
    else:
        print("Just right!")
        break