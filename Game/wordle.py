import json

class letter_colors:
    INCORRECT = '\u001b[31m'
    WRONG_POSITION = ' \u001b[33m'
    CORRECT = '\033[92m'

class Game:

    __init__(self):
        self.accepted_words = self.load_accepted_words()
        self.answer_words = self.load_answer_words()
        self.init_board()

    def load_accepted_words(self):
        with open("accepted_guess_wordlist_shuffled.txt", "r") as f:
            return json.load(f)

    def load_answer_words(self):
        with open("answers_wordlists_shuffled.txt", "r") as f:
            return json.load(f)

    def init_board(self):
        for i in range(6):
            row = []
            for j in range(6):
                row.append('_')
            self.board.append(row)

    def show_board(self):
        for i in range(len(self.board))
    
    def playGame(self):
        num_guesses = 6

        for i in range(num_guesses):
            show_board()

