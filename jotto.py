import random
import ujson as json
from tqdm import tqdm

def compute_jots(actual_word,guess_word):
	return len(set(actual_word) & set(guess_word))

## Gather five letter words with unique letters
# words = json.load(open('words_dictionary.json','r'))
# five_letter_words = []
# for word in words:
# 	if len(word) == 5:
# 		if len(set(word))==5:
# 			five_letter_words.append(word)
# with open('five_letter_words.json','w') as f:
# 	f.write(json.dumps(five_letter_words))
# print("dumped {} words".format(len(five_letter_words)))

## Gather five letter words from top 100000
# five_letter_words = []
# with open('google-10000-english-no-swears.txt','r') as f:
# 	for line in f:
# 		word = line.strip()
# 		if len(word) == 5:
# 			if len(set(word)) == 5:
# 				five_letter_words.append(word)
# with open('five_letter_words.json','w') as f:
# 	f.write(json.dumps(five_letter_words))
# print("dumped {} words".format(len(five_letter_words)))

## Build jotto map
five_letter_words = json.load(open('five_letter_words.json'))
# one_change_map = {}
# for word1 in tqdm(five_letter_words):
#     if word1 not in one_change_map:
#         one_change_map[word1] = {}
#     for j, word2 in enumerate(five_letter_words):
#         if word1 == word2:
#             continue
#         leftLetter = list(set(word1) - set(word2))
#         if len(leftLetter) != 1:
#             continue
#         rightLetter = list(set(word2) - set(word1))
#         letters = [leftLetter[0],rightLetter[0]]
#         letters = sorted(letters)
#         change = ','.join(letters)
#         if change not in one_change_map[word1]:
#         	one_change_map[word1][change] = []
#         if word2 not in one_change_map[word1][change]:
# 	        one_change_map[word1][change].append(word2)
# with open('one_change_map.json','w') as f:
# 	f.write(json.dumps(one_change_map))




def play_jotto(jotto_word,current_guess):
	print("playing with " + jotto_word)
	one_change_map = json.load(open('one_change_map.json'))
	knowledge = {}
	finished_letters = {}
	guesses = [current_guess]
	jots = {}
	jots[current_guess] = compute_jots(jotto_word,current_guess)

	for i in range(0,300):
		print(jotto_word,guesses[i],jots[guesses[i]])
		available_changes = {}
		for guess in guesses:
			for change in one_change_map[guess].keys():
				new_change = True
				for letter in change.split(','):
					if letter in finished_letters:
						new_change = False
				if not new_change:
					continue
				if change not in available_changes:
					available_changes[change] = []
				available_changes[change].append(guess)
		# print('available changes: ')
		# print(available_changes)
		while True:
			next_guess_change = random.choice(list(available_changes.keys()))
			next_guess_from = random.choice(available_changes[next_guess_change])
			next_guess = random.choice(one_change_map[next_guess_from][next_guess_change])
			if next_guess in guesses:
				continue
			guesses.append(next_guess)
			break


		jots[guesses[i+1]] = compute_jots(jotto_word,guesses[i+1])
		leftLetter = list(set(next_guess_from) - set(guesses[i+1]))[0]
		rightLetter = list(set(guesses[i+1]) - set(next_guess_from))[0]
		print(f'{next_guess_from} ({jots[next_guess_from]}) -> {guesses[i+1]} ({jots[guesses[i+1]]})')
		if jots[guesses[i+1]] > jots[next_guess_from]:
			new_knowledge = ['+'+rightLetter,'-'+leftLetter]
		elif jots[guesses[i+1]] < jots[next_guess_from]:
			new_knowledge = ['-'+rightLetter,'+'+leftLetter]
		else:
			continue
		for k in new_knowledge:
			knowledge[k] = True
			finished_letters[rightLetter] = True
			finished_letters[leftLetter] = True
		print('gained new knowledge: ' + ' '.join(new_knowledge))
		if len(finished_letters) == 10:
			return i

jotto_word = random.choice(five_letter_words)
jotto_word = 'boats'
starting_guess = random.choice(five_letter_words)
for i in range(10):
	print(play_jotto(jotto_word,starting_guess))
