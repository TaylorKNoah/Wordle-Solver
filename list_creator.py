# used to randomize the answer list so I don't spoil it all
from copy import deepcopy
from math import floor
from random import shuffle
import json


with open("./accepted_guess_list_raw.txt", 'r') as f:
    words = f.read()

words = words[1:]
length = len(words)
ten_percent = floor(length / 10)
print(ten_percent)
word_list = []
print(words[0])

i = 0
k = 0
print("Creating list.")
for i in range(len(words)):
    if i % ten_percent == 0:
        print(f'{i / ten_percent*10}% ...')

    if words[i] == '"':
        if k%2 == 0 and words[i+1] != "]":
            k += 1
            j = i+1
            while(words[j]!='"'): j += 1
            word = words[i+1:j]
            word_list.append(deepcopy(word))
        else:
            k += 1

shuffle(word_list)
print(len(word_list))
print(word_list[:6])

print("Generating new file for list...")
with open("accpeted_guess_wordlist_shuffled.txt", 'w') as f:
    json.dump(word_list, f)

print("Finished!")

