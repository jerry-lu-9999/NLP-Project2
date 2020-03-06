# CSC247/447 Project 2: Intention/Goal Recognition

## Description

Based on the weighted abductive reasoning we learned in lecture, the goal of this project is to write a program that can match a sequence of given observations to plans, and output a list of goals/intents corresponding to those plans. 

Specifically, you're given:

1) a list of consecutive observations, which are triples of words in the TRIPS lexicon. 

2) a plan library with a list of plans. Each plan consists of sequences of actions associated with a goal - both the actions and the goal are triples. The first element of a triple is always a TRIPS ontology type, and the rest of the elements are variables followed by ontology type restrictors.

When you match an observation to an action, you should replace the variable with the *word* it was matched to, everywhere in the plan that variable occurs. For each list of observations, your code should output a list of the goals/intents which explain the observations with the *lowest cost* (particularized with the words that were matched) after all observations have been seen. For weighted abduction, assume that the cost of assuming each goal is 1 (i.e. all are equally likely).

In the case of multiple observations, your code should maintain a list of all instantiated plans. Given a new observation, you can either "continue" filling in a semi-instantiated plan (if the match succeeds), or you can instantiate a new plan from the plan library (even if this is another copy of a plan which was already instantiated).

See the following sections for some more clarifications, and the section **"Task Details"** below for more information about what you're expected to implement.

## Examples

Given a plan library
```
goal: (ONT::STEAL ?x:ONT::PERSON ?z:ONT::FACILITY)
acts: (ONT::MOTION ?x:ONT::PERSON ?z:ONT::FACILITY)
      (ONT::BODY-MANIPULATION ?x:ONT::PERSON ?y:ONT::WEAPON)
      (ONT::DIRECTIVE ?x:ONT::PERSON ?w:ONT::MONEY)
      (ONT::DEPART ?x:ONT::PERSON ?z:ONT::FACILITY)

```
and an observation

```
(travel partner store)
```

the result of matching the observation to this plan (specifically, the first act) would be an instantiated plan where we substitute the word for the variable.

```
goal: (ONT::STEAL partner store)   
acts: (ONT::MOTION partner store)
      (ONT::BODY-MANIPULATION partner ?y:ONT::WEAPON)
      (ONT::DIRECTIVE partner ?x:ONT::MONEY)
      (ONT::DEPART partner store)
```

given another observation

```
(grasp partner gun)
```

it's possible to continue "filling in" the instantiated plan (making the goal/intent more likely, i.e. lower cost):

```
goal: (ONT::STEAL partner store)   
acts: (ONT::MOTION partner store)
      (ONT::BODY-MANIPULATION partner gun)
      (ONT::DIRECTIVE partner ?x:ONT::MONEY)
      (ONT::DEPART partner store)
```

however, if instead the second observation was

```
(grasp person gun)
```

Matching the already instantiated plan would fail, since "person" does not equal "partner". But it could instantiate and match a new copy of the plan:

```
goal: (ONT::STEAL person ?z:ONT::FACILITY)
acts: (ONT::MOTION person ?z:ONT::FACILITY)
      (ONT::BODY-MANIPULATION person gun)
      (ONT::DIRECTIVE person ?w:ONT::MONEY)
      (ONT::DEPART person ?z:ONT::FACILITY)

```

## Notes

1. Word sense disambiguation in context

As discussed in the lecture slides, some words are ambiguous and can have multiple ontology types. For example, the word `partner` can map to two different TRIPS ontology types: `ONT::AFFILIATE` and `ONT::FAMILY-RELATION`. This means `(travel partner store)` can match either `(ONT::MOVE ?x:ONT::PERSON ?z:ONT::FACILITY)` or `(ONT::MOVE ?x:ONT::AFFILIATE ?z:ONT::FACILITY)`.

In this case, your code should keep both possibilities and attempt to match them both, so that future observations may be used to disambiguate.


2. Intention recognition with minimal covering explanation

Your goal is to find the best actions with the least commitment and the least cost. Use the following functions as we discussed in lecture:
```
cost(P ∨ Q) = min(cost(P), cost(Q))
cost(P & Q) = cost(P) + cost(Q)
```

## Task Details

For this project, you may additionally use the `pytrips` library, which provides an interface for accessing the TRIPS ontology and doing operations like subsumption checks. Details on how to use it are available in `demo.ipynb` (open in Jupyter notebook).

### Part 1

Implement the functionality described above in the function `recognize_intent`, defined in `code.py`. This function should take as input a list of observations (each observation is a tuple of strings representing words), and output a list of goals/intents (each goal is a tuple of strings representing ontology types, variables, or words).

#### More Implementation Details

To implement the function `recognize_intent`, please follow the details below.

Your function should be finding the *most general* lowest-cost solution. If you have three possible conclusions (where a conclusion is either
an assumed intent, or a conjunction of assumed intents) which all have the same cost, and this cost is also the lowest cost, your function should return a disjunction of these three conclusions.

For the return value, please use the following format:

- the return value should be a list of lists.
- the outer list is to be interpreted as a disjunction.
- the inner lists are to be interpreted as conjunctions.

For example, if your singular lower-cost solution is `(ONT::STEAL partner store)`, then your function should return 
```
[[('ONT::STEAL', 'partner', 'store')]]
```

If your lowest-cost solutions are `(ONT::STEAL friend airport),(ONT::DEPART friend ?y:ONT::COUNTRY)`,

i.e. meaning the same as `(ONT::STEAL friend airport) v (ONT::DEPART friend ?y:ONT::COUNTRY)`, 

then your function should return
```
[[('ONT::STEAL', 'friend', 'airport')], [('ONT::DEPART', 'friend', '?y:ONT::COUNTRY')]]
```

If your lowest-cost solutions are

`((ONT::STEAL person airport) (ONT::BECOME person ?w:ONT::PROFESSIONAL)), ((ONT::DEPART person ?y:ONT::COUNTRY) (ONT::BECOME person ?w:ONT::PROFESSIONAL))`, 

i.e. meaning the same as

`((ONT::STEAL person airport) & (ONT::BECOME person ?w:ONT::PROFESSIONAL)) v ((ONT::DEPART person ?y:ONT::COUNTRY) & (ONT::BECOME person ?w:ONT::PROFESSIONAL))`, 

then your function should return
```
[[('ONT::STEAL', 'person', 'airport'), ('ONT::BECOME', 'person', '?w:ONT::PROFESSIONAL')],
[('ONT::DEPART', 'person', '?y:ONT::COUNTRY'), ('ONT::BECOME', 'person', '?w:ONT::PROFESSIONAL')]]
```

To maintain backwards compatibility with before this clarification was released, a single flat list of tuples will be interpreted as a disjunction.

#### Testing

Feel free to define any additional functions you need in `code.py`, but *do not* create any additional Python files outside of that one.

We've provided a list of example inputs in `input/observations_test.txt`, and the corresponding "gold" outputs in `output/intents_test.txt`. Each line in the input specifies a comma-separated list of observations (in the order they occur). The output uses the CSV format indicated above (i.e. the one where commas represent disjunctions and spaces between tuples represent conjunctions). An action library is provided for these test examples in `input/plan_libraries/plan_library_test.json`.

To test your code, run `python3 test.py` from the root directory.

### Part 2

Provide **three** of your own examples (expanding the plan library as necessary to support these examples), where **at least one** of the examples involves multiple observations.

Create any new plans in `input/plan_libraries/plan_library_custom.json`, and write your three example inputs in `input/observations_custom.txt`, and the expected outputs in `output/intents_custom.txt`. Make sure the format is the same as in the examples that are given to you.

NOTE: the [Trips web interface](https://www.cs.rochester.edu/research/trips/lexicon/browse-ont-lex-ajax.html) might be useful for creating the examples.

## Submission

Submit a `[yourname].zip` file on Blackboard. Make sure that you've implemented the skeleton code in the `code.py` file, and have included your custom plans and 3 example inputs/outputs in the `input/plan_libraries/plan_library_custom.json`, `input/observations_custom.txt`, and `output/intents_custom.txt` files, respectively.

Please include a `README.{txt|pdf}` file in your submission. This file should contain your **name**, **student ID**, and **email** in a header. Give a short outline of your implementation of the algorithms, and any additional commentary you feel is necessary (any specific running instructions, known issues/bugs your code has, etc.)

## Acknowledgement

Thanks to Rik Bose for providing us with PyTrips demo. 
