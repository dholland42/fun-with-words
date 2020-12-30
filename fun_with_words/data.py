"""A module for parsing the raw dictionary file into structured data."""

def parse_book(book):
    words = dict()
    word = ""
    defn = []
    first_complete = False
    for row in book:
        row = row.strip()
        if not row:
            continue
        if row.isupper():
            words[word] = defn
            word = row
            defn = []
            continue
        defn.append(row.split(".")[0])
    return words
