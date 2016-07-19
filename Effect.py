import re
from Formula import Formula

class Effect:
    def __init__(self, text):
        self.parse_effect(text)

    def parse_effect(self, text):
        """Populate Effect object from game CSV file entry format string.

        Args:
            text (str): String representation of effect from game CSV file.
        
        Raises:
            ValueError: If the text does not conform to the expected pattern.

        Note:
            Some of the original game Effect strings were malformed.
            Known effect error cases:
                Both values inside parens:
                    _security_,(0.025+0.035*x)
                    _security_,(0.025+0.038*x)
                    _security_,(0.05+0.05*x)
                    _security_,(0.075+0.1*x)
                Extra decimal point:
                    Equality,0.0.5+(0.15*x)
                Missing comma:
                    Religious-0.06-(0.06*x)
                Missing left parenthesis:
                    Liberal,0+0.10*x)
                    Wages,-0.12+0.24*x)
                    Socialist,0.02+0.08*x)
                Parentheses around third term:
                    Religious,-0.12-0.62*(x^2.2)
        
        """
        # parse out the stuff from text
        # [target],[v1][op1]([v2][op2][v3])[op4][v4],[inertia]
        # [target],[value1][operator1]
        # ([value2][operator2][values3])[operator3][value4],[inertia]
        binop = r'([+\-*/\^])'# binary operator
        flnum = r'([+\-]?\d+(?:\.\d*)?)' # signed decimal number
        tvar = r'(\w?)'
        fort =  r'([+\-]?\d+(?:\.\d*)?|[\w\s]+?)' # decimal or target name
        pat = ''.join((r'([\w\s]+),\s*', flnum, binop,
                       r'\(', fort, binop, fort, r'\)',
                       r'(?:', binop, flnum, r')?,?(\d+)?'))
        p = re.compile(pat)
        m = p.match(text)
        try:
            g = m.groups()
        except AttributeError:
            raise ValueError()
        else:
        # [target],[v1][op1]([v2][op2][v3])[op4][v4],[inertia]
            self.__dict__.update(dict(
                target = g[0], v1 = g[1],
                op1 = g[2], v2 = g[3], op2 = g[4],
                v3 = g[5], op3 = g[6], v4 = g[7], intertia = g[8]))
        self.fmla = Formula(self.v1, self.v2, self.v3, self.v4,
                            self.op1, self.op2, self.op3)

    def reprint(self):
        """Represent the Effect as a string in game CSV format."""
        return ''.join((self.target, " ", self.v1, self.op1,
                        "(", self.v2, self.op2, self.v3, ")",
                        (self.op3 or ""), (self.v4 or ""),
                        '; ', str(self.fmla.minmax()[0]),
                        ' to ', str(self.fmla.minmax()[1])))

    def __str__(self):
        return (self.target + "," + str(self.fmla))
