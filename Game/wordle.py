import json
from copy import deepcopy
import os
from termcolor import colored
from random import randint
from StatAgent import StatAgent

class letter_colors:
    DEFAULT = 'white'
    INCORRECT = 'red'
    WRONG_POSITION = 'yellow'
    CORRECT = 'green'

class Game:
    def __init__(self, player=0):
        os.system('color')

        self.accepted_words = self.load_accepted_words()
        self.answer_words = self.load_answer_words()
        self.ensure_all_answers_in_accepted_list()

        self.board = []
        self.board_mask = []
        self.keys = 'abcdefghijklmnopqrstuvwxyz'
        self.key_mask = []

        self.init_board()
        # for board coloring
        self.init_board_color_mask()
        self.init_key_mask()
        
        if player == 1:
            self.agent = StatAgent(self.accepted_words)
        
        if player != 0:
            self.known_letters = ['?', '?', '?', '?', '?']

        

    def load_accepted_words(self):
        with open("accepted_guess_wordlist_shuffled.txt", "r") as f:
            return json.load(f)

    def load_answer_words(self):
        with open("answers_wordlist_shuffled.txt", "r") as f:
            return json.load(f)
    
    def ensure_all_answers_in_accepted_list(self):
        for word in self.answer_words:
            if word not in self.accepted_words:
                self.accepted_words.append(word)
        


    def init_board(self):
        for i in range(6):
            row = []
            for j in range(5):
                row.append('_')
            self.board.append(deepcopy(row))
            row.clear()
    
    def init_board_color_mask(self):
        for i in range(6):
            row = []
            for j in range(5):
                row.append(letter_colors.DEFAULT)
            self.board_mask.append(deepcopy(row))
            row.clear()

    def init_key_mask(self):
        for i in range(len(self.keys)):
            self.key_mask.append(letter_colors.DEFAULT)
    
    def update_key_mask(self, word, answer):
        for i in range(len(word)):
            idx = self.keys.index(word[i])
            
            if word[i] == answer[i]: self.key_mask[idx] = letter_colors.CORRECT
            elif word[i] in answer: self.key_mask[idx] = letter_colors.WRONG_POSITION
            else: self.key_mask[idx] = letter_colors.INCORRECT
    

    def show_keys(self):
        print()
        for i in range(len(self.keys)):
            print(colored(self.keys[i], self.key_mask[i]), end=' ')


    def show_board(self):
        for i in range(len(self.board)):
            print()
            for j in range(len(self.board[i])):
                print(colored(self.board[i][j], self.board_mask[i][j]), end=' ')

    def word_not_valid(self, word):
        if word == None: return True

        if word not in self.accepted_words:
            print('Not an accepted word.')
            return True
        
        return False
    
    def get_player_guess(self, player=0):
        word = None
        if player == 0:
            word = self.get_user_word()

        # stat agent
        elif player == 1:
            letters_left = self.get_available_letters()
            word = self.agent.make_guess(letters_left, self.known_letters)

        return word
    
    def get_user_word(self):
        return(input("\n\nEnter your guess here: "))
    
    def get_available_letters(self):
        available_letters = []
        for i in range(len(self.keys)):
            if self.key_mask[i] != letter_colors.INCORRECT:
                available_letters.append(self.keys[i])
        
        return available_letters

    def update_known_letters(self, word, current_guess):
        for i in range(len(self.board_mask[current_guess])):
            if self.board_mask[current_guess][i] == letter_colors.CORRECT:
                self.known_letters[i] = word[i]


    def input_word(self, word, guess_num):
        for i in range(len(word)):
            self.board[guess_num][i] = word[i]
    

    def update_mask(self, word, answer, current_guess):
        for i in range(len(word)):
            if word[i] == answer[i]: self.board_mask[current_guess][i] = letter_colors.CORRECT
            elif word[i] in answer: self.board_mask[current_guess][i] = letter_colors.WRONG_POSITION
            else: self.board_mask[current_guess][i] = letter_colors.INCORRECT
    
    def has_won(self, guess, answer):
        if guess == answer:
            return True
        return False



    def playGame(self, player):
        num_guesses = 6
        winner = False
        prev_word = None

        answer = self.answer_words[randint(0,len(self.answer_words)-1)]

        if(player!=0):
            print(f'The agent is hoping to find the word: {answer}!')
            print(f'Lets see if it can...')

        if answer not in self.accepted_words:
            print(f'Gunna have a hard time finding this word since the answer isnt allowed as a guess...')

        self.show_keys()
        print()
        self.show_board()

        for current_guess in range(num_guesses):
            if(self.has_won(prev_word, answer)): break

            word = None
            while self.word_not_valid(word):
                word = self.get_player_guess(player)
            
            self.input_word(word, current_guess)
            self.update_mask(word, answer, current_guess)
            self.update_key_mask(word, answer)

            if player != 0:
                self.update_known_letters(word, current_guess)

            prev_word = word

            self.show_keys()
            print()
            self.show_board()
        

        if current_guess < num_guesses:
            print("\n\n Congratulations!!")
        else:
            print("\n\n Better luck next time.")
        
        print("The correct word was: "+answer)
       


#test
game = Game(1)
game.playGame(1)