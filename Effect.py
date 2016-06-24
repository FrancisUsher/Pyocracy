import re
from Formula import Formula

class Effect:
    def __init__(self, text):
        self.parse_effect(text)

    def parse_effect(self, text):
        # parse out the stuff from text
        # [target],[value1][operator1]
        # ([value2][operator2][values3])[operator3][value4],[inertia]
        binop = r'([+\-*/\^])'
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
            # print(text)
            """Known effect error cases:
            # both values inside parens
            _security_,(0.025+0.035*x)
            _security_,(0.025+0.038*x)
            _security_,(0.05+0.05*x)
            _security_,(0.075+0.1*x)
            # extra decimal point
            Equality,0.0.5+(0.15*x)
            # missing comma
            Religious-0.06-(0.06*x)
            # missing left paren
            Liberal,0+0.10*x)
            Wages,-0.12+0.24*x)
            Socialist,0.02+0.08*x)
            # parens around third term
            Religious,-0.12-0.62*(x^2.2)
            """
            # Erroneous Effect, handled gracefully
            raise ValueError()
        else:
            self.__dict__.update(dict(
                target = g[0], v1 = g[1],
                op1 = g[2], v2 = g[3], op2 = g[4],
                v3 = g[5], op3 = g[6], v4 = g[7], intertia = g[8]))
        self.fmla = Formula(self.v1, self.v2, self.v3, self.v4,
                            self.op1, self.op2, self.op3)

    def reprint(self):
        return ''.join((self.target, " ", self.v1, self.op1,
                        "(", self.v2, self.op2, self.v3, ")",
                        (self.op3 or ""), (self.v4 or ""),
                        '; ', str(self.fmla.minmax()[0]),
                        ' to ', str(self.fmla.minmax()[1])))

    def __str__(self):
        return (self.target + "," + str(self.fmla))

    #def max_order(self):
        # find highest order of magnitude in expression
        # where's the var? according to pat in parse_effect, v2 or v3
