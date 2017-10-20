# Independent-Weighted-Knapsack
This function approximates the best possible combination of items to purchase and resell in the NP-hard problem Independent Weighted Knapsack, which is a combination of Weighted Knapsack and Independent Set.

The context for the problem is we enter a store with N items, where every item has a cost and resale value. The objective is to choose a list of items maximize our profit, which is defined as the sum of the resale values minus the sum of the costs.

We have constraints. We have a budget of M; the sum of the costs of our chosen items can't exceed M. We have a carrying capacity P; every item has a weight and the sum of weights mustn't exceed P. Finally, we have C different constraint classes, which are C different lists of elements such that we can't simultaneously select multiple items from the same constraint class. One item may be in arbitrarily many constraint classes.

Input :

N items (which all have a weight, cost, and resale value).
P: Our maximum weight-carrying-capacity,
M: Our maximum budget,
C: The number of different constraint classes
And a list of the constraints. Each constraint is a set of elements that cannot be selected concurrently.
Output :

The list of items that maximizes profit given the constraints.

## Main Idea:
I implemented a relatively straightforward greedy algorithm that does one pass through the items. Starting with the item of highest profit, which we define as resale value minus cost, and in descending order by profit, we try to add all good looking items into our sack. I used Python’s simple multiprocessing library to parallelize threads on my machine.
## More Detail:
I take a greedy approach in one pass through the items. I begin by sorting the list of items by their [profit = resale value – cost], in order of largest to smallest profit.
Iterating over the items in that order, I throw out any items with a negative profit, because it is never advantageous to choose such an item. In addition, I throw out any items whose addition to our sack will go over the weight or budget constraints, as well as any items whose item-class has a conflict with a class already in the set of chosen items. If an item passes these conditions, we add it to our set of chosen items and record any newly constrained item-classes. In short, this is a simple stochastic greedy algorithm that favors items with the better [resale value – cost] value.
By increasing the number of iterations, we can get good approximations
## Runtime Analysis:
	Our algorithm first sorts the item using profit as the relative order, descending. Using Python’s built in sort method means this takes Ѳ(N logN) time. We then iterate over the N items for sale until reaching items with negative profit (as soon as it finds the first, it ends iteration). 
For every item in the iteration, we check a few conditions, ensuring positive profit and that the item fits in the Gargsack within budget and weight requirements. We also check if the item’s class is constrained by previous items. We use a python set data structure for this task, which makes this operation reliably run in constant time. We then must update our constrained set of item-class to exclude item-classes that are in the same constraint group as the new item. To do this, I preprocessed a mapping (python dictionary) from each item to the indices corresponding to the constraint sets that it is a part of, so that I can directly iterate over an item’s constraint classes, rather than necessarily have to iterate over every constraint class at each iteration (though that is still the worst case behavior). I then use the python set union operation to incorporate the new constraints into our constrained items. The union operation takes linear time. I never union the same constraint more than once, because I make sure not to repeat this costly operation if I already enforced the constraints for the new item by adding a previous item from its class. Therefore the total runtime from constraint-checking throughout the entirety of the algorithm will grow linearly with the sum over all constraints of the number of item-classes in each constraint, which is upper bounded by Ѳ(N*M) in the worst case where almost every item is in every constraint, and this is Ѳ(M) in the best case where constraints have a constant upper bound on number of classes in them.
The most expensive parts of the algorithm are constraint checking and sorting. The runtime is approximately Ѳ(N*(M + LogN)) in the worst case or Ѳ(M + N*LogN).
## Performance: 
Though this algorithm can in theory achieve optimality sometimes, the greediness has very bad performance against some adversarial input. Some instances of the problem have more Independent Set nature than Weighted Knapsack nature, and my solution is better at solving Weighted Knapsack natured instances. For example, if the item with the highest profit was constrained against every other item, we would take it instead of every other item, no matter how bad of a choice that is; so this algorithm’s proportion to optimal cannot be bounded at all. I could have improved on this by choosing a different greedy heuristic other than profit, or by looking ahead further in terms of whether an item is not worth its class constraints.
