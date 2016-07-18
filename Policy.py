from Effect import Effect

"""name
   guiname
   slider
   description
   flags
   introduce
   cancel
   raise
   lower
   department
   mincost
   maxcost
   cost multiplier
   implementation
   minincome
   maxincome
   incomemultiplier
"""

class Policy:
    def __init__(self, row, heads):
        self.parse_policy(row, heads)

    def parse_policy(self, row, heads):
        """Populate the policy object based on a row of the game Policies CSV.
        Keyword arguments:
            row: Sequence of values from a game Policies CSV row.
            heads: Names for each value in a prefix of the row.
        """
        self.__dict__.update({h:v for (h,v) in zip(heads, row)})
        self.effects = parse_effects((val for val in split_effects(row)))
        
    def parse_effects(effects):
        for val in effects:
            if val.strip(): # Don't use any empty effects
                try:
                    yield Effect(val)
                except ValueError:
                    # Malformed Effect string, ignore it and parse the rest.
                    # See comment above Effect class for known errors cases.
                    pass

    # returns true if one of the effects, 
    def has_effect(self, search_effects):
        return any(any(term in e.target for e in self.effects)
                   for term in search_effects)

def split_effects(vals):
    for (i, val) in enumerate(vals[:-1]):
        if '#effects' in val.lower():
            return vals[i+1:]
    return []
