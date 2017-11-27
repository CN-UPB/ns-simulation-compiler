# parser for .vec files of Omnet++
import csv
import numpy as np
import scipy as sp
import scipy.stats
import matplotlib.pyplot as plt


# from https://stackoverflow.com/a/15034143/2745116
def mean_confidence_interval(data, confidence=0.95):
	a = 1.0*np.array(data)
	n = len(a)
	m, se = np.mean(a), scipy.stats.sem(a)
	h = se * sp.stats.t.ppf((1+confidence)/2., n-1)
	return m, m-h, m+h


# take single vector in CSV spreadsheet format, parse and return float dict (time->value)
def parse_vector(vector_csv):
	vector = {}
	with open(vector_csv, "r") as csv_file:
		reader = csv.reader(csv_file)
		for row in reader:
			if len(row) == 2:
				try:
					vector[float(row[0])] = float(row[1])
				except ValueError:
					print(f"Skipping {row[0]}, {row[1]} (can't convert to float)")
	return vector;


# TODO: automatically parse one large csv with multiple vectors inside
# file = "delay.csv"
# parse and plot end-to-end delay for different cache hit probabilities
folder = "analysis/eval/"
vecs = ["delay7-3.csv", "delay8-2.csv", "delay9-1.csv"]
stats = []
means = []

for v in vecs:
	v_parsed = parse_vector(folder + v)
	v_stats = mean_confidence_interval(list(v_parsed.values()))
	print(f"{v}: {v_stats}")
	stats.append(v_stats)
	means.append(v_stats[0])


# TODO: prettier plots
plt.plot(vecs, means)
plt.show()
