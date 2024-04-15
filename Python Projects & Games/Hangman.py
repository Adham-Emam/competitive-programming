import sys
import requests


def main():
    # Here the user is asked to enter the name first
    name = input("What is your name? ")

    # Select the level of difficulty

    levels = [1, 2, 3]

    # make sure that the user typed an integer
    while True:
        try:
            level = int(input(f"Pick the level of difficulty {levels}: "))

            set_level(level, name)
            break

        except ValueError:
            print(f"\nPlease pick a number from {levels}")


# function will generate random word from an API
def get_random_word():
    try:
        # API to get a random word
        url = "https://random-word-by-api-ninjas.p.rapidapi.com/v1/randomword"

        headers = {
            "X-RapidAPI-Key": "06432802d1msh93264aa61476401p14dc2ajsn6bb6b7f21cd5",
            "X-RapidAPI-Host": "random-word-by-api-ninjas.p.rapidapi.com",
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            word = response.json()
            return word["word"]
        else:
            sys.exit(f"Failed to get random word. Status code: {response.status_code}")
    except requests.RequestException as e:
        sys.exit(f"Error making API request: {e}")


# Set a suitable word for the difficulty
def set_level(level, name):
    random_word = get_random_word()

    word_length = len(random_word)
    if (
        (level == 1 and word_length <= 7)
        or (level == 2 and 7 < word_length <= 10)
        or (level == 3 and word_length > 10)
    ):
        print("Good Luck ! ", name)
        start_game(random_word, level)
    else:
        set_level(level, name)


def start_game(word, level):
    print("Guess the characters")
    print()
    guesses = []

    # number of turns depending on level
    turns = {1: 10, 2: 7, 3: 5}.get(level)

    while turns > 0:

        # counts the number of times a user fails
        failed = 0

        # all characters from the input
        # word taking one at a time.
        for char in word:

            # comparing that character with
            # the character in guesses
            if char in guesses:
                print(char, end=" ")

            else:
                print("_", end=" ")

                # for every failure 1 will be
                # incremented in failure
                failed += 1
        print()
        print()
        print("letters remaining to guess: ", failed)
        print("already used letters: ", guesses)

        if failed == 0:
            # user will win the game if failure is 0
            # and 'You Win' will be given as output
            print("You Win")

            # this print the correct word
            print("The word is: ", word)
            break

        # User guess input with some rules
        while True:
            guess = input("Guess a character: ")

            # Check the input from the user is unique
            # Ensure that the user type only on letter and its an alphabet
            if guess not in guesses and guess.isalpha() and len(guess) == 1:
                break
            else:
                if guess.lower() in guesses:
                    print("Try a different letter")
                elif not guess.isalpha():
                    print("Please type a letter from the alphabet")
                elif len(guess) != 1:
                    print("Please type only one letter per try")

        print()

        # every input character will be stored in guesses
        guesses += guess.lower()

        # check input with the character in word
        if guess not in word.lower():

            turns -= 1

            # if the character doesn’t match the word
            # then “Wrong” will be given as output
            print("Wrong")

            # this will print the number of
            # turns left for the user
            print("You have", +turns, "more guesses")

            if turns == 0:
                print(f"You Lose, the word is {word}")


if __name__ == "__main__":
    main()
