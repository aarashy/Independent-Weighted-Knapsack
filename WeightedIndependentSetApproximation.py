#!/usr/bin/env python

from __future__ import division
import argparse, random
from multiprocessing import Pool
import numpy as np


def solve(P, M, N, C, items, constraints, j):
    """
    This function approximates the best possible combination of items to purchase and resell
    in the NP-hard problem which is a combination of Weighted Knapsack and Independent Set.

    Given:
    N items (which all have a weight, cost, and resale value).
    P: Our maximum weight-carrying-capacity,
    M: Our maximum budget,
    C: The number of different constraint classes
    and a list of the constraint classes, such that we can't pick two items in the same class.

    This function approximates the combination of items to purchase and resell which yields highest profit.
    """
    print("Starting Problem " + str(j))
    NUM_ITERATIONS = 50
    bestItems = []
    bestProfit = -float("inf")
    set_iters = int(N ** 0.6)
    MAINDISTR = DiscreteDistribution()
    
    for z in range(NUM_ITERATIONS):
        if z == NUM_ITERATIONS/2:
            print("half done with problem : " + str(j) + ", So far we got" + str(bestProfit))
        itemz = items[:]
        items_chosen = []
        constrained = set()
        totalWeight = 0
        totalCost = 0
        totalProfit = 0
        for i in range(set_iters):
            index = np.random.randint(len(itemz))
            item = itemz[index]
            itemz.remove(item)
            if ((totalWeight + item[2] < P) & (totalCost + item[3] < M) & (item[1] not in constrained)):
                totalWeight += item[2]
                totalCost += item[3]
                totalProfit += item[4] - item[3]
                for constraint in constraints:
                    if item[1] in constraint:
                        constrained = (constrained | constraint) - set([item[1]])
                items_chosen.append(item[0])

        for item in sorted(itemz, key=getKey, reverse=True):
            if ((totalWeight + item[2] < P) & (totalCost + item[3] < M) & (item[1] not in constrained)):
                totalWeight += item[2]
                totalCost += item[3]
                totalProfit += item[4] - item[3]
                for constraint in constraints:
                    if item[1] in constraint:
                        constrained = (constrained | constraint) - set([item[1]])
                items_chosen.append(item[0])
        if totalProfit > bestProfit:
            bestProfit = totalProfit
            bestItems = items_chosen
    print("Found a bestProfit for problem " + str(j) + ": " + str(bestProfit))
    return bestItems

def getKey(item):
  return (item[4]-item[3])

def read_input(filename):
	"""
	P: float
	M: float
	N: integer
	C: integer
	items: list of tuples
	constraints: list of sets
	"""
	with open(filename) as f:
		P = float(f.readline())
		M = float(f.readline())
		N = int(f.readline())
		C = int(f.readline())
		items = []
		constraints = []
		for i in range(N):
			name, cls, weight, cost, val = f.readline().split(";")
			items.append((name, int(cls), float(weight), float(cost), float(val)))
		for i in range(C):
			constraint = set(eval(f.readline()))
			constraints.append(constraint)
		return P, M, N, C, items, constraints

def write_output(filename, items_chosen):
    with open(filename, "w") as f:
		for i in items_chosen:
			f.write("{0}\n".format(i))

class DiscreteDistribution(dict):
    """
    A DiscreteDistribution models weight distributions
    over a finite set of discrete keys.
    """
    def __getitem__(self, key):
        self.setdefault(key, 0)
        return dict.__getitem__(self, key)

    def copy(self):
        """
        Return a copy of the distribution.
        """
        return DiscreteDistribution(dict.copy(self))

    def argMax(self):
        """
        Return the key with the highest value.
        """
        if len(self.keys()) == 0:
            return None
        all = self.items()
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]

    def total(self):
        """
        Return the sum of values for all keys.
        """
        return float(sum(self.values()))

    def normalize(self):
        """
        Normalize the distribution such that the total value of all keys sums
        to 1. The ratio of values for all keys will remain the same. In the case
        where the total value of the distribution is 0, do nothing.

        >>> dist = DiscreteDistribution()
        >>> dist['a'] = 1
        >>> dist['b'] = 2
        >>> dist['c'] = 2
        >>> dist['d'] = 0
        >>> dist.normalize()
        >>> list(sorted(dist.items()))
        [('a', 0.2), ('b', 0.4), ('c', 0.4), ('d', 0.0)]
        >>> dist['e'] = 4
        >>> list(sorted(dist.items()))
        [('a', 0.2), ('b', 0.4), ('c', 0.4), ('d', 0.0), ('e', 4)]
        >>> empty = DiscreteDistribution()
        >>> empty.normalize()
        >>> empty
        {}
        """
        _sum = self.total()
        for item in self.keys():
            self[item] = self[item]/_sum

    def sample(self):
        """
        Draw a random sample from the distribution and return the key, weighted
        by the values associated with each key.

        >>> dist = DiscreteDistribution()
        >>> dist['a'] = 1
        >>> dist['b'] = 2
        >>> dist['c'] = 2
        >>> dist['d'] = 0
        >>> N = 100000.0
        >>> samples = [dist.sample() for _ in range(int(N))]
        >>> round(samples.count('a') * 1.0/N, 1)  # proportion of 'a'
        0.2
        >>> round(samples.count('b') * 1.0/N, 1)
        0.4
        >>> round(samples.count('c') * 1.0/N, 1)
        0.4
        >>> round(samples.count('d') * 1.0/N, 1)
        0.0
        """
        r = random.random()
        _total = self.total()
        for key in self.keys():
            r -= self[key]/_total
            if r <= 0:
                return key
def solver(i):
    print("../project_instances/problem" + str(i) + ".in")
    P, M, N, C, items, constraints = read_input("../project_instances/problem" + str(i) + ".in")
    write_output("../output/problem" + str(i) + ".out", solve(P, M, N, C, items, constraints, i))

if __name__ == "__main__":
	#pool = Pool(processes=3)
	#pool.map(solver, range(1, 4))
    solver(18)
    #parser = argparse.ArgumentParser(description="PickItems solver.")
    #parser.add_argument("input_file", type=str, help="____.in")
    #parser.add_argument("output_file", type=str, help="____.out")
    #args = parser.parse_args()