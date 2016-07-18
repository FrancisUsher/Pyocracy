from D3Parser import parse_effects_from_row



class Policy:
    """

    Attributes:
        name (str): Internal unique identifier.
        guiname (str): How it should be called in-game.
        slider: 
        description (str): How it should be described in-game.
        flags: 
        introduce: Political capital cost to introduce.
        cancel: Political capital cost to cancel.
        raise: Political capital cost to raise.
        lower: Political capital cost to lower.
        department: Which policy category this falls under.
            We might want to extend this to more general policy tags so
            users can organize the screen in custom views, not just the
            7 default departments.
        mincost: Cost to fund policy at minimum.
        maxcost: Cost to fund policy at maximum.
        cost multiplier
        implementation
        minincome
        maxincome
        incomemultiplier
        effects (list): Formulas for how this policy affects the game situation.
    """
    def __init__(self, row, heads):
        """Populate the policy object based on a row of the game Policies CSV.
        Keyword arguments:
            row: Sequence of values from a game Policies CSV row.
            heads: Names for each value in a prefix of the row.
        """
        self.__dict__.update({h:v for (h,v) in zip(heads, row)})
        self.effects = parse_effects_from_row(row)

    def has_effect(self, search_effects):
        """Check if the policy affects any of the search_effect tagets."""
        return any(any(term in e.target for e in self.effects)
                   for term in search_effects)


