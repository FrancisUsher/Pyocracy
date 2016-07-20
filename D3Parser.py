from Effect import Effect
from itertools import dropwhile

"""Parser for the Democracy 3 game files"""

def parse_effects_from_row(row):
    effects = parse_effects((val for val in split_effects(row)))
    return list(effects)

def parse_effects(effects):
    """Turn effect string representations into Effect objects.

    Args:
        effects (iterable): Unparsed effect entry strings.

    Yields:
        Effect: The next effect parsed from the input.
        
    """
    for val in effects:
        if val.strip(): # Don't use any empty effects
            try:
                yield Effect(val)
            except ValueError:
                # Malformed Effect string, ignore it and parse the rest.
                # See comment above Effect class for known problem cases.
                pass

def split_effects(vals):
    """The effects are all the values that come after the entry "#Effects"."""
    effects = dropwhile(lambda x:'#effects' not in x.lower(), vals[:-1])
    next(effects)
    return effects
