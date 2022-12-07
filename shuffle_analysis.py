#!/usr/bin/env python3
import sys
from itertools import chain, count
from functools import reduce

def weave(deck):
	half = len(deck) // 2
	return list(chain.from_iterable(zip(deck[:half], deck[half:])))

def shuffles_required(deck_size):
	starting_deck = list(range(deck_size))
	current_shuffle = starting_deck
	for i in count(start=1):
		current_shuffle = weave(current_shuffle)
		if current_shuffle == starting_deck:
			return i

def main():
	max_size = 200
	deck_sizes = range(2, max_size+1, 2)
	results = reduce(
		lambda res, deck_size: res + [(deck_size, shuffles_required(deck_size))],
		deck_sizes,
		[]
	)	

	print(results)

if __name__ == '__main__':
	sys.exit(main())
