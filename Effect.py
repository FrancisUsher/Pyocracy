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
        """An effect takes the form:
            [target],[v1][op1]([v2][op2][v3])[op3][v4],[inertia]
        where v1-v4 are float values or variables
        and op1-op3 are binary arithmetic operators.
        op3 and v4 are optional and usually used for exponentiation
        """
        binop = r'([+\-*/\^])'# binary operator
        flnum = r'([+\-]?\d+(?:\.\d*)?)' # signed decimal number
        tvar = r'([\w\s]+)'
        prefix = tvar + r',\s*'
        prefix_op = flnum + binop
        inner_op = r'\(' + fort + binop + fort + r'\)'
        suffix_op = r'(?:' + binop + flnum + r')?'
        suffix = r',?(\d+)?'
        fort =  r'([+\-]?\d+(?:\.\d*)?|[\w\s]+?)' # decimal or target name
        pat = ''.join((prefix, prefix_op, inner_op, suffix_op, suffix))
        p = re.compile(pat)
        m = p.match(text)
        try:
            g = m.groups()
        except AttributeError:
            raise ValueError()
        else:
        # [target],[v1][op1]([v2][op2][v3])[op4][v4],[inertia]
            self.__dict__.update(zip(['target', 'v1', 'op1', 'v2', 'op2',
                                      'v3', 'op3', 'v4', 'intertia'], g[:9]))
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
