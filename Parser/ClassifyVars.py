from ModalLogic import *


def free_vars(term):
    if isinstance(term, Variable):
        return {term}

    elif isinstance(term, Constant):
        return set()

    elif isinstance(term, Abstraction):
        return free_vars(term.body) - {term.var}

    elif isinstance(term, Application):
        return set.union(free_vars(term.operator),free_vars(term.operand))

    elif isinstance(term, Predicate):
        return set()

    elif isinstance(term, PredicateFormula):
        return set.union(free_vars(term.predicate), *[free_vars(arg) for arg in term.arguments])

    elif isinstance(term, Conjunction):
        return set.union(free_vars(term.left) , free_vars(term.right))

    elif isinstance(term, HornClause):
        return set.union(free_vars(term.head), *[free_vars(body) for body in term.body])

    elif isinstance(term, ExistentialQuantifier):
        return free_vars(term.body) - {term.var}

    elif isinstance(term, UniversalQuantifier):
        return free_vars(term.body) - {term.var}

    elif isinstance(term, Biconditional):
        return set.union(free_vars(term.left) , free_vars(term.right))

    elif isinstance(term, HornClause):
        return set.union(free_vars(term.antecedent) , free_vars(term.consequent))

    elif isinstance(term, Disjunction):
        return set.union(free_vars(term.left) , free_vars(term.right))

    elif isinstance(term, Negation):
        return free_vars(term.term)

    elif isinstance(term, Necessity):
        return free_vars(term.term)

    elif isinstance(term, Possibility):
        return free_vars(term.term)

    else:
        return term


def bound_vars(term):
    if isinstance(term, Identifier):
        return set()

    elif isinstance(term, Abstraction):
        return set.union({term.var} , bound_vars(term.body))

    elif isinstance(term, Application):
        return set.union(bound_vars(term.operator) , bound_vars(term.operand))

    elif isinstance(term, Predicate):
        return set()

    elif isinstance(term, PredicateFormula):
        return set.union(bound_vars(term.predicate), *[bound_vars(arg) for arg in term.arguments])

    elif isinstance(term, Conjunction):
        return set.union(bound_vars(term.left) , bound_vars(term.right))

    elif isinstance(term, HornClause):
        return set.union(bound_vars(term.head), *[bound_vars(body) for body in term.body])

    elif isinstance(term, ExistentialQuantifier):
        return set.union({term.var} , bound_vars(term.body))

    elif isinstance(term, UniversalQuantifier):
        return set.union({term.var} , bound_vars(term.body))

    elif isinstance(term, Biconditional):
        return set.union(bound_vars(term.left) , bound_vars(term.right))

    elif isinstance(term, HornClause):
        return set.union(bound_vars(term.antecedent) , bound_vars(term.consequent))

    elif isinstance(term, Disjunction):
        return set.union(bound_vars(term.left) , bound_vars(term.right))

    elif isinstance(term, Negation):
        return bound_vars(term.term)

    elif isinstance(term, Necessity):
        return bound_vars(term.term)

    elif isinstance(term, Possibility):
        return bound_vars(term.term)

    else:
        return term


def all_vars(term):
    return set.union(free_vars(term) , bound_vars(term))
