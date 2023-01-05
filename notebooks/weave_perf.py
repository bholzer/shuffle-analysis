# Databricks notebook source
from itertools import chain, count
from functools import reduce
import numpy as np
from time import perf_counter

# COMMAND ----------

def zip_weave(deck):
	half = len(deck) // 2
	return list(chain.from_iterable(zip(deck[:half], deck[half:])))

def rev_weave(deck):
	pairs = [ deck[i:i+2] for i in range(0,len(deck),2) ]
	reversed_pairs = map(lambda l: np.flip(l), pairs)
	return list(chain.from_iterable(reversed_pairs))


def shuffles_required(deck_size, weave_func):
	start_time = perf_counter()
	starting_deck = list(range(deck_size))
	current_shuffle = starting_deck
	for i in count(start=1):
		current_shuffle = weave_func(current_shuffle)
		if current_shuffle == starting_deck:
			end_time = perf_counter()
			print(f'Shuffling {deck_size} items {i} times took {end_time - start_time:0.4f}s')
			return i


# COMMAND ----------

shuffles_required(29930, zip_weave)

# COMMAND ----------

shuffles_required(29930, rev_weave)