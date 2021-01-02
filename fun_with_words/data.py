"""A module for parsing the raw dictionary file into structured data."""

import os
import pathlib
import itertools
import collections

STARTLINE = 27
ENDLINE = 973904

def get_full_dataset(filename=os.path.join(pathlib.Path(os.path.abspath(__file__)).parent.parent, "data/dictionary.txt")):
    with open(filename, encoding="utf-8") as f:
        raw_data = f.readlines()[STARTLINE:ENDLINE]
    words = defns(raw_data, lambda x: x[0].isalnum())
    data = [(d, word) for (word, defn) in words.items() for d in defn]
    return data


def canonical_lines(raw_data):
    current = ""
    started = False
    for row in raw_data:
        row = row.strip()
        if not row:
            if current:
                yield current.strip()
                current = ""
        elif row.isupper():
            yield row
        else:
            current += " " + row

def get_pairs(data):
    word = ""
    defs = []
    for row in data:
        if row.isupper():
            if word:
                for w in word.split(";"):
                    if len(w.split()) == 1:
                        yield w.strip(), defs
            word = row
            defs = []
        elif row.lower().startswith("defn:"):
            for d in row[5:].split(".")[0].split(";"):
                if not d.strip().startswith("See "):
                    defs.append(d.strip().lower())
    for w in word.split(";"):
        if len(w.split()) == 1:
            yield w.strip(), defs

def defns(raw_data, filter_func=lambda x: True):
    words = collections.defaultdict(lambda : list())
    for word, defn in filter(filter_func, get_pairs(canonical_lines(raw_data))):
        if defn:
            words[word.lower()].extend(defn)
    return words

