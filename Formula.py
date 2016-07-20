import re

class Formula:
    def __init__(self, v1, v2, v3, v4, op1, op2, op3):
        (self.v1, self.v2, self.v3, self.v4) = (v1, v2, v3, v4)
        (self.op1, self.op2, self.op3) = (op1, op2, op3)
        fun1 = lambda x: op_to_func(op1)(float(v1), x)
        first_var = v2.isalpha()
        first = lambda x: op_to_func(op2)(x, float(v3))
        second = lambda x: op_to_func(op2)(float(v2), x)
        fun2 = first if first_var else second
        if op3:
            fun3 = lambda x: op_to_func(op3)(x, float(v4))
            sec_prec = (op3 == '^' or op1 == '+'
                     or (op3 in '*/' and not op1 == '^'))
            if sec_prec:
                self.fun = lambda x: fun1(fun3(fun2(x)))
            else:
                self.fun = lambda x: fun3(fun1(fun2(x)))
        else:
            self.fun = lambda x: fun1(fun2(x))

    def parse_formula(self, text):
        """Extract text representation of formula into member variables.

        This duplicates functionality in the Effect class. This version
        seems not to be currently used, however the functionality probably
        belongs in this class in the long-term.
        """
        # parse out the stuff from text
        # [value1][operator1]([value2][operator2][values3])[operator3][value4]
        binop = r'([+\-*/\^])' # binary operator
        flnum = r'([+\-]?\d+(?:\.\d*)?)' # signed decimal number
        fort =  r'([+\-]?\d+(?:\.\d*)?|[\w\s]+?)' # decimal or target name
        pat = ''.join((flnum, binop, r'\(', fort, binop, fort, r'\)',
                       r'(?:', binop, flnum, r')?'))
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
            # also in at least one case a source target name
            # is given as a coefficient instead of a variable name
            """
            # Malformed Formula, handle gracefully somewhere else please
            raise ValueError(' '.join(["Unexpected Formula format", text]))
        self.__dict__.update(zip(['v1', 'op1', 'v2', 'op2', 'v3', 'op3', 'v4'],
                                 g[1:8]))
        self.fmla = Formula(self.v1, self.v2, self.v3, self.v4,
                            self.op1, self.op2, self.op3)

    def __str__(self):
        return ''.join((self.v1, self.op1,
                        "(", self.v2, self.op2, self. v3, ")",
                        (self.op3 or ""), (self.v4 or "")))

    def minmax(self):
        return (self.fun(0), self.fun(1))

def op_to_func(op):
    if op == '+':
        return (lambda x, y: x + y)
    elif op == '-':
        return (lambda x, y: x - y)
    elif op == '*':
        return (lambda x, y: x * y)
    elif op == '/':
        return (lambda x, y: x / y)
    elif op == '^':
        return (lambda x, y: x ** y)

