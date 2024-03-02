import Utils
import LambdaUtils

class Conjunction(LambdaTerm):
    def __init__(self, *conjuncts):
        self.conjuncts = conjuncts

    def __str__(self):
        return f"{' ∧ '.join(map(str, self.conjuncts))}"

def and_(*terms):
    flattened = []
    for term in terms:
        if isinstance(term, Conjunction):
            flattened.extend(term.conjuncts)
        else:
            flattened.append(term)
    return Conjunction(*flattened)

from typing import Union, Tuple, Dict, Set

class Term:
    pass

class Constant2(Term):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Variable2(Term):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)

Binding = Dict[Variable, Constant]


class BinaryPredicate:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)


def relation(*names):
    return definition_macro_builder(names, BinaryPredicate)

# def variable(*names):
#     return definition_macro_builder(names, lambda name: f'Variable("{name}")')
#
# def constant(*names):
#     return definition_macro_builder(names, lambda name: f'Constant("{name}")')

class Formula:
    pass

class BinaryPredicateFormula(Formula):
    def __init__(self, predicate, arguments):
        self.predicate = predicate
        self.arguments = arguments

    def __str__(self):
        return  f"{self.predicate}({', '.join(map(str, self.arguments))})"


class HornClause:
    def __init__(self, *formulas):
        self.antecedent = Conjunction(*formulas[:-1])
        self.consequent = formulas[-1]

    def __str__(self):
        return f"{self.antecedent} ⟹ {self.consequent}"


class ExistentialQuantifier:
    def __init__(self, var, formula):
        self.var = var
        self.formula = formula

    def __str__(self):
        return f"∃{self.var}.{self.formula}"


def apply_binding(formula: Union['Constant', 'Variable', 'BinaryPredicateFormula', 'Conjunction'],
                  binding: Dict) -> Union['Constant', 'Variable', 'BinaryPredicateFormula', 'Conjunction']:
    if isinstance(formula, Constant):
        return formula
    elif isinstance(formula, Variable):
        return binding.get(formula, formula)
    elif isinstance(formula, BinaryPredicateFormula):
        return BinaryPredicateFormula(formula.predicate, tuple(apply_binding(arg, binding) for arg in formula.arguments))
    elif isinstance(formula, Conjunction):
        return Conjunction(*(apply_binding(conjunct, binding) for conjunct in formula.conjuncts))
    else:
        return formula


class Necessity:
    def __init__(self, formula):
        self.formula = formula

    def __str__(self):
        return f"□ {self.formula}"

class Possibility:
    def __init__(self, formula):
        self.formula = formula

    def __str__(self):
        return f"◇ {self.formula}"

class ModalFormula:
    def __init__(self, operator, formula):
        self.operator = operator
        self.formula = formula

    def __str__(self):
        return f"{self.operator}{self.formula}"


class Negation:
    def __init__(self, formula):
        self.formula = formula

    def __str__(self):
        return f"¬({self.formula})"

class Disjunction:
    def __init__(self, formula1, formula2):
        self.formula1 = formula1
        self.formula2 = formula2

    def __str__(self):
        return f"({self.formula1} ∨ {self.formula2})"

class Biconditional:
    def __init__(self, formula1, formula2):
        self.formula1 = formula1
        self.formula2 = formula2

    def __str__(self):
        return f"({self.formula1} ⇔ {self.formula2})"

class UniversalQuantifier:
    def __init__(self, variable, formula):
        self.variable = variable
        self.formula = formula

    def __str__(self):
        return f"(∀{self.variable}.{self.formula})"


