from pytrips import ontology
import json
import sys
import copy

ont = ontology.load()

"""
The skeleton file. You should implement your code here. Make sure that the code you write here runs properly
when called by the test.py file in the root directory.

Feel free to add any import statements above, AS LONG AS the package is jsontrips, pytrips, or any
package in the Python standard library.

Feel free to write any additional functions you need in this file, but DO NOT create any new Python files.
"""

def recognize_intent(observations):
  """Takes observations as input: this is a list of tuples of the form (word1, word2, word3), where each
     tuple represents an observation (listed in order of occurrence). Return a list of lists (interpreted as
     described in the guidelines), e.g. [[('ONT::STEAL', 'partner', 'store'), ('ONT::TARGET_PRACTICE', 'person', 'gun')]]"""
  
  plan_library = read_plan_library() # Read plan library from files in input/plan_libraries

  for tup in observations:
    #(travel partner store)
    ob_1, ob_2, ob_3 = tup
    temp_value = sys.maxsize
    num_of_tuple = len(observations)
    list_of_library = []
    for num in range(num_of_tuple):
      list_of_library.append(copy.deepcopy(plan_library))

    for library in list_of_library:
      final_list = []
      for dict in library:
        goal = dict['goal']
        list_as_goal = list(goal)
        ont_2 = list_as_goal[1][3:]; ont_3 = list_as_goal[2][3:]
        for element in ont["w::" + ob_2]:
          if (element < ont[ont_2] or element == ont[ont_2]):
            list_as_goal[1] = ob_2
        for element in ont["w::" + ob_3]:
          if (element < ont[ont_3] or element == ont[ont_3]):
            list_as_goal[2] = ob_3
        temp_list = []
        goal = tuple(list_as_goal)
        temp_list.append(goal)
        print(goal)

        acts = dict['acts']
        #"(ONT::MOTION ?x:ONT::PERSON ?z:ONT::FACILITY)",
        for tup_str in acts:  #tup_str is a tuple
          list_as_tup = list(tup_str)
          ont_1 = list_as_tup[0];ont_2 = list_as_tup[1];   ont_3 = list_as_tup[2]
          ont_2 = ont_2[3:]
          ont_3 = ont_3[3:]
          a = False; b = False

          #1st check the first ontology
          for element in ont["w::" + ob_1]:
            if (element < ont[ont_1] or element == ont[ont_1]):
              #if it matches, then we replace
              for element in ont["w::" + ob_2]:
                if (element < ont[ont_2] or element == ont[ont_2]):
                  list_as_tup[1] = ob_2
                  a = True
              for element in ont["w::" + ob_3]:
                if (element < ont[ont_3] or element == ont[ont_3]):
                  list_as_tup[2] = ob_3
                  b = True
          tup_str = tuple(list_as_tup)
          print(tup_str)
          #meaning that there's change been made
          if a == True and b == True:
            if temp_list not in final_list:
              final_list.append(temp_list)

        print()

  return final_list

def if_matched(tup, tup_str):
  tup_strcopy = copy.deepcopy(tup_str)
  list_obser = list(tup)     #observation tuple
  list_as_tup_str = list(tup_str)
  for i in range(len(list_as_tup_str)):
    if list_as_tup_str[i][0] == '?':
      list_as_tup_str[i] = list_as_tup_str[i][3:]
    if i == 0: continue
    for element in ont["w::"+ list_obser[i]]:
      if element < ont[list_as_tup_str[i]] or element == ont[list_as_tup_str[i]]:
        list_as_tup_str[i] = list_obser[i] 
  tup_str = tuple(list_as_tup_str)
  if tup_strcopy == tup_str:
    return False
  else:
    return True

def parse_tuple_string(str):
  """Parses a string representing a tuple into a tuple of strings."""
  strs = str.strip().strip('(').strip(')').split( )
  return (strs[0].lower(), strs[1].lower(), strs[2].lower())


def list_tuple_string(st):
  """Parses a string representing a tuple into list of a tuple of strings. """
  strs = st.strip().strip('(').strip(')').split()
  l = []
  l.append((strs[0].lower(), strs[1].lower(), strs[2].lower()))
  return l


def read_plan_library():
  """Reads in plan library from plan library files."""
  # Define file paths to load from
  plan_library_test = 'input/plan_libraries/plan_library_test.json'
  plan_library_custom = 'input/plan_libraries/plan_library_custom.json'
  plan_library = []
  # Read test plan library
  with open(plan_library_test) as f:
    plans_test = json.load(f)
    plan_library += [{'goal':parse_tuple_string(plan['goal']),
                      'acts':list(map(parse_tuple_string, plan['acts']))} for plan in plans_test]
  # Read custom plan library
  with open(plan_library_custom) as f:
    plans_custom = json.load(f)
    plan_library += [{'goal':parse_tuple_string(plan['goal']),
                      'acts':list(map(parse_tuple_string, plan['acts']))} for plan in plans_custom]
  return plan_library
  
