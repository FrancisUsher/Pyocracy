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
        self.__dict__.update({h:v for (h,v) in zip(heads, row)})
        self.effects = []
        for val in splitfx(row):
            if val.strip():
                try:
                    self.effects.append(Effect(val))
                except ValueError:
                    # Erroneous Effect, handled gracefully
                    # See comment above Effect class for known errors
                    pass

    # returns true if one of the effects, 
    def has_effect(self, search_fx):
        return any(any(term in e.target for e in self.effects)
                   for term in search_fx)

def splitfx(vals):
    for (i, val) in enumerate(vals[:-1]):
        if '#effects' in val.lower():
            return vals[i+1:]
    return []
