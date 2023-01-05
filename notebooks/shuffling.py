# Databricks notebook source
from itertools import chain, count
from functools import reduce
import matplotlib.pyplot as plt
import csv
from numpy import interp
from multiprocessing import Pool
from time import perf_counter

# COMMAND ----------

def weave(deck):
	half = len(deck) // 2
	return list(chain.from_iterable(zip(deck[:half], deck[half:])))

def shuffles_required(deck_size):
	start_time = perf_counter()
	starting_deck = list(range(deck_size))
	current_shuffle = starting_deck
	for i in count(start=1):
		current_shuffle = weave(current_shuffle)
		if current_shuffle == starting_deck:
			end_time = perf_counter()
			print(f'Shuffling {deck_size} items {i} times took {end_time - start_time:0.4f}s')
			return i

# Wrap shuffles_required for parallelization
def shuffles_for_deck_size(deck_size):
	return (deck_size, shuffles_required(deck_size))


# COMMAND ----------

deck_min_size = 2
deck_max_size = 20000
deck_sizes = range(deck_min_size, deck_max_size+1, 2)

# COMMAND ----------

results = Pool(processes=64).map(shuffles_for_deck_size, deck_sizes)

# COMMAND ----------

x = [ data[0] for data in results ]
y = [ data[1] for data in results ]
plt.plot(x, y, 'ro', markersize=3.0)
plt.xlabel('Deck Size')
plt.ylabel('Shuffle Count')
plt.grid()
plt.show()
