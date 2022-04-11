from Alphabet import Alphabet as alpha
from copy import deepcopy
from random import randint
import os

class StatAgent:

	def __init__(self, acceptable_guess_words):
		self.word_list = acceptable_guess_words
		self.total_letter_frequencies = self.init_freqs()
		self.letter_pos_freqs = self.init_pos_freqs()
	

	def init_freqs(self):
		letter_freqs = []
		for i in range(26):
			letter_freqs.append(0)

		for word in self.word_list:
			for letter in word:
				try:
					letter_freqs[(alpha.valueOf(letter))-1] += 1
				except:
					print(f'Error: StatAgent.Init_Freqs: word: ({word}), letter: ({letter}), alpha_idx: ({alpha.valueOf(letter)})')
		
		for i in range(26):
			letter_freqs[i] /= len(self.word_list)
		
		return letter_freqs

	def init_pos_freqs(self):
		pos_freqs = []
		for i in range(26):
			pos_freqs.append([0,0,0,0,0])

		for word in self.word_list:
			for idx, letter in enumerate(word):
				let_idx = alpha.valueOf(letter)
				try:
					pos_freqs[let_idx-1][idx] += 1
				except:
					print(f'Error StatAgent.Init_Pos_Freqs --> Letter Index in Word: ({let_idx}), Letter Index in Alphabet: ({idx})')
					print(f'IndexError: list index out of range')
					os.abort()
		
		for i in range(26):
			for j in range(5):
				pos_freqs[i][j] /= len(self.word_list)
		
		return pos_freqs
	
	def make_guess(self, letters_left, known_letters, half_known_letters={}):
		print(f'\n\nAgent is making a guess...')
		print(f'Available letters: {letters_left}')
		print(f'Number of words in acceptable words: {len(self.word_list)}')

		word_bag = self.get_valid_words(letters_left, known_letters, half_known_letters)

		word_values = []
		for i in range(len(word_bag)):
			word_values.append(0)
		
		# get values of words based on commonality of used letters
		for idx, word in enumerate(word_bag):
			found_letters = []
			for letter in word:
				lower_letter = letter.lower()
				if lower_letter in found_letters:
					continue
				word_values[idx] +=  self.total_letter_frequencies[alpha.valueOf(lower_letter)-1]
				found_letters.append(lower_letter)
			found_letters.clear()

		print(f'Possible words: {word_bag[0:5]}')
		print(f'Word values based on letters: {word_values[0:5]}')
		
		# get values of position of letters
		for idx, word in enumerate(word_bag):
			for letter_idx, letter in enumerate(word):
				word_values[idx] += self.letter_pos_freqs[alpha.valueOf(letter)-1][letter_idx]
		

		print(f'Word values based on letters and positions: {word_values[0:5]}')
		
		# make list of highest values word(s)
		max_word_val = max(word_values)
		highest_val_words = []
		for idx, word in enumerate(word_bag):
			if word_values[idx] == max_word_val:
				highest_val_words.append(word)

		print(f'Highest value words: {highest_val_words}')
		

		#randomly choose fromhighest value words - could use neighbor likliness here to improve
		r = randint(0, len(highest_val_words)-1)
		print(f'Guessed word: {highest_val_words[r]}')
		return highest_val_words[r]
		

	def get_valid_words(self, letters_left, known_letters, half_known_letters={}):
		valid_words = []

		for word in self.word_list:
			valid_word = True
			for letter in word:
				if letter not in letters_left:
					valid_word = False
					break
			if valid_word:
				valid_words.append(word)
		
		# check if any known letters
		for i in range(len(known_letters)):
			if known_letters[i] != '?':
				valid_words = self.keep_words_with_kown_letters(valid_words, known_letters)
				break
		
		if half_known_letters != {}:
			valid_words = self.filter_half_known_letters(half_known_letters, valid_words)

		return valid_words

	def keep_words_with_kown_letters(self, valid_words, known_letters, i=0):
		# knwon letters is form like: [s, h, ?, ?, ?]
		# recursively filter out words that do not have known letters

		if i > 4: return valid_words

		print(f'Len valid words BEFORE finding words with known letters @index({i}): {len(valid_words)}')
		print(f'Known letter @ {i}: {known_letters[i]}')
		to_keep = []

		if known_letters[i] != '?':
			print(f'Searching for words with ({known_letters[i]} @ {i}.')
			for j in range(len(valid_words)):
				if valid_words[j][i] == known_letters[i]:
						to_keep.append(valid_words[j])
		else:
			return self.keep_words_with_kown_letters(valid_words, known_letters, (i+1))

		print(f'Len valid words AFTER finding words with known letters @index({i}): {len(to_keep)}')

		return self.keep_words_with_kown_letters(to_keep, known_letters, (i+1))
	
	def filter_half_known_letters(self, half_knowns, valid_words, i=0, j=0, ):
		if i >= len(half_knowns): return valid_words

		to_keep = []

		for word in valid_words:
			if word[half_knowns[i][1][j]] != half_knowns[i][0]:
				to_keep.append(word)
		
		if j < len(half_knowns[i][1]):
			return self.filter_half_known_letters(half_knowns, valid_words, i, j+1)
		
		return self.filter_half_known_letters(half_knowns, valid_words, i+1, 0)
