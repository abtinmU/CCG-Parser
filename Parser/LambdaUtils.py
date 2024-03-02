from typing import Union, Set
import Utils

# Types #

class LambdaTerm:
    pass

class Constant(LambdaTerm):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Variable(LambdaTerm):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)

Identifier = Union[Constant, Variable]

class Abstraction(LambdaTerm):
    def __init__(self, var, body):
        self.var = var
        self.body = body

    def __str__(self):
        return f"λ{self.var}.({self.body})"

class Application(LambdaTerm):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __str__(self):
        return f"({self.operator})({self.operand})"

def operator(app: Application):
    return app.operator

def operand(app: Application):
    return app.operand

# Construction Sugar and IO #

def variable(*names):
    return def_builder(names, "Variable")

def constant(*names):
    return def_builder(names, "Constant")

def lambda_(var, body):
    if isinstance(var, Variable):
        return Abstraction(var, body)
    else:
        if isinstance(body, LambdaTerm):
            return lambda_(Variable(var), body)
        else:
            return lambda_(Variable(var), Variable(body))

def apply(operator, operand):

    if isinstance(operator, LambdaTerm):
        if isinstance(operand, LambdaTerm):
            return Application(operator, operand)
        else:
            return operator(Variable(operand))
    elif isinstance(operator, Predicate):
        if isinstance(operand, LambdaTerm):
            return PredicateFormula(predicate, operand)
    else:
        if isinstance(operand, LambdaTerm):
            return apply(Variable(operator),operand)
        else:
            return apply(Variable(operator),Variable(operand))



def rename_var(term, frm, to):
    if isinstance(term, Identifier):
        if term == frm:
            return to
        else:
            return term
    elif isinstance(term, Abstraction):
        return lambda_(rename_var(term.var, frm, to), rename_var(term.body, frm , to))
        # return Abstraction(rename_var(term.var, frm, to), substitute(term.body, frm, to))
    elif isinstance(term, PredicateFormula):
        return PredicateFormula(rename_var(term.predicate, frm, to), *[rename_var(arg, frm, to) for arg in term.arguments])
    elif isinstance(term, Application):
        return apply(rename_var(term.operator, frm, to), (rename_var(term.operand, frm, to)))
        # return Application(substitute(app.operator, frm, to), substitute(app.operand, frm, to))
    elif isinstance(term, Conjunction):
        return and_(*(rename_var(t, frm, to) for t in term.conjuncts))
    else:
        return term


def replacement(term, frm, to):

    if isinstance(term, Constant):
        return term

    elif isinstance(term, Variable):
        if term == frm:
            return to
        else:
            return term

    elif isinstance(term, Abstraction):
        if term.var == frm:
            return term
        elif term.var not in free_vars(to) and frm not in free_vars(term):
            return lambda_(term.var, replacement(term.body, frm, to))
        else:
            new_var = gen_new_var(term, to, frm)
            return lambda_(new_var, replacement(rename_var(term.body, term.var, new_var), frm, to))

    elif isinstance(term, Application):
        return apply(replacement(term.operator, frm, to), (replacement(term.operand, frm, to)))

    elif isinstance(term, PredicateFormula):
        return PredicateFormula(replacement(term.predicate, frm, to), *[replacement(arg, frm, to) for arg in term.arguments])
    elif isinstance(term, Conjunction):
        return and_(*(replacement(t, frm, to) for t in term.conjuncts))
    else:
        return term


# beta reduce operator and operand as much as possible
def chek_oper_App_or_Abs(operator, operand):

    if (isinstance(operator, Application) | isinstance(operand, Application)) == True:

          if (isinstance(operator, Application) & isinstance(operand, Application)) == True:
              return beta_reduce(operator), beta_reduce(operand)

          if isinstance(operator, Application):
              operator2 = beta_reduce(operator)
          else:
              operator2 = operator

          if isinstance(operand, Application):
              operand2 = beta_reduce(operand)
          else:
              operand2 = operand

          return operator2, operand2
    else:
        operator2 = operator
        operand2 = operand

    if ((operator2 == operator) & (operand2 == operand)) == True:
        return operator2, operand2
    if (isinstance(operator2, Application) | isinstance(operand2, Application)) == True:
        chek_oper_App_or_Abs(operator, operand)


class Predicate:
    def __init__(self, name):
        self.name = Constant(name)

    def __str__(self):
        return str(self.name)

def predicate(*args):
    clean_names = [str(name).split('.')[-1] for name in args[:-1]]
    arity = args[-1]
    for name, clean_name in zip(args[:-1], clean_names):
        globals()[clean_name] = Predicate(clean_name)

class PredicateFormula(LambdaTerm):
    def __init__(self, predicate, *arguments):
        self.predicate = predicate
        self.arguments = arguments

    def __str__(self):
        args_str = ' '.join(map(str, self.arguments))
        return f"{self.predicate}({args_str})"
