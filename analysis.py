import csv
import re
from Policy import Policy

# Retrieve all effects of every 
def all_effects(rows):
    effects = []
    for row in rows:
        effect = False
        for val in row:
            if effect:
                effects.append(val.split(',')[0])
            elif val == '#Effects':
                effect = True
    return sorted(set(effects))

class Analysis:
    def __init__(self, path):
        self.c = csv.reader(open(path))
        self.rows = [line for line in self.c]
        self.d = self.dicify() # list of attr-keyed dicts of policies

    # take first line of csv values and apply it as keys to each row
    # the effects list is partitioned off separately for each row
    def dicify(self):
        return {row[1]:Policy(row, self.rows[0]) for row in self.rows[1:]}
        
    def load_attrs(self, efx):
        self.attrs = [x for x in all_effects(self.rows)
                      if any(effect in x for effect in efx)]

    # Put the names and matching policies in member
    def select_policies(self, search_fx):
        self.selected = {p.guiname:
                         [e.reprint() for e in p.effects
                          if any(term in e.target for term in search_fx)]
                    for p in self.d.values() if p.has_effect(search_fx)}

    def print_selected(self):
        if not self.selected.keys():
            return
        n = max(len(k) for k in self.selected.keys())
        for (name, effects) in self.selected.items():
            print(name + '  ::')
            print('\t' + '\n\t'.join(effects))
            #print('{} :: {}'.format(name.ljust(n), ';'.join(effects)))

    def query_attrs(self, terms):
        self.load_attrs(terms)
        self.select_policies(terms)
        self.print_selected()

    """def query_policy(self, pol):
        matches = [k for k in self.d.keys() if pol in k]
        for m in matches:
            print (m + ' ::')
            print ('\t' + '\n\t'.join(e.reprint() for e in d[m][effects]))"""

versions = ['vanilla', 'socialengineering', 'extremism', 'clones']

#interesting = ['freq', 'global', 'ncome']
interesting = ['ncome']
results = [Analysis(p+'\\policies.csv') for p in versions]
#attrs = sorted(set.union(*[set(a.attrs) for a in eighs]))
