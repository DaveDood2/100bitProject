import itertools
import functools
import re

def findInList(item, list):
    # Returns a list of the indeces that an item occurs in list
    # Referenced from: https://stackoverflow.com/questions/6294179/how-to-find-all-occurrences-of-an-element-in-a-list
    return [i for i, x in enumerate(list) if x == item]

# We wrap the original python map and reduce functions to be more powerful and resilient
def mapSequential(data, func):
    return list(map(func, data))

def reduceSequential(data, func):
    return functools.reduce(func, data)

def reduceByKeySequential(data, func):
    reduced_data = []
    for key, vals in itertools.groupby(sorted(data, key=lambda x: x[0]), key=lambda x: x[0]):
        reduced_data.append((key, reduceSequential([x[1] for x in vals], func)))
    return reduced_data

def flatMapSequential(data, func):
    mapped_data = mapSequential(data, func)
    flattened_data = [item for lst in mapped_data for item in lst]
    return flattened_data

# Given a key and value, return a (key, value) pair
def makeKeyValue(key, value=1):
    if (key == ''):
        key = -1
    return (key, value)

def addValues(a, b):
    return a+b

# Given a comma list, return an iterable of numbers
def splitCommaList(listItem):
    # Referenced from: https://stackoverflow.com/questions/7844118/how-to-convert-comma-delimited-string-to-list-in-python
    #print("test!", listItem.split(","))
    #return [int(e) for e in listItem.split(",") if e.isdigit()]
    #if (skipBlank == False):
    return [int(e) if e.isdigit() else e for e in listItem.split(',')]
    #else:
    #    return list([int(e) for e in listItem.split(',') if e.isdigit()])

    