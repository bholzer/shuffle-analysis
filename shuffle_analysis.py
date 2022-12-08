#!/usr/bin/env python3
import sys
from itertools import chain, count
from functools import reduce
import matplotlib.pyplot as plt
import csv
import argparse
from numpy import interp

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

def write_to_csv(results, file_name):
	with open(file_name, 'w', newline='') as csv_file:
		fieldnames = ['deck_size', 'shuffle_count']
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		writer.writeheader()
		for r in results:
			writer.writerow({ 'deck_size': r[0], 'shuffle_count': r[1] })

def main():
	args = parse_args()
	deck_sizes = range(args.min, args.max+1, 2)
	results = reduce(
		lambda res, deck_size: res + [ (deck_size, shuffles_required(deck_size)) ],
		deck_sizes,
		[]
	)

	out_file_name = f'{args.min}-{args.max}'

	if args.data_out:
		write_to_csv(results, f'data/{out_file_name}.csv')

	if args.plot_out:
		x = [ data[0] for data in results ]
		y = [ data[1] for data in results ]
		plt.plot(x, y, 'ro', markersize=3.0)
		plt.xlabel('Deck Size')
		plt.ylabel('Shuffle Count')
		plt.grid()
		plt.savefig(f'images/{out_file_name}.png', bbox_inches='tight', dpi=200)

def parse_args():
	parser = argparse.ArgumentParser(description='Do an analysis of perfect shuffles on various deck sizes')
	parser.add_argument(
		'-m',
		'--min',
		type=int,
		default=2,
		help='Minimum deck size to check, must be an even number'
	)
	parser.add_argument(
		'-n',
		'--max',
		type=int,
		default=1000,
		help='Maximum deck size to check, must be an even number'
	)
	parser.add_argument(
		'-d',
		'--data-out',
		action=argparse.BooleanOptionalAction,
		help='File to write results to in CSV format'
	)
	parser.add_argument(
		'-p',
		'--plot-out',
		action=argparse.BooleanOptionalAction,
		help='Write plot to file'
	)

	return parser.parse_args()

if __name__ == '__main__':
	sys.exit(main())
