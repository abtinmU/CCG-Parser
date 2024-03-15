from LambdaCalculus import *

from typing import Union, List

class Direction:
    pass

class Right(Direction):
    pass

class Left(Direction):
    pass

class SyntacticType:
    def __str__(self):
        return self.__class__.__name__

    def __truediv__(self, other: 'SyntacticType'):
        return ComplexSyntacticType(self, other, Right())

    def __floordiv__(self, other: 'SyntacticType'):
        return ComplexSyntacticType(other, self, Left())

    def agrees_with(self, other):
        return False

class ComplexSyntacticType(SyntacticType):
    def __init__(self, res: SyntacticType, arg: SyntacticType, direction: Direction):
        self.res = res
        self.arg = arg
        self.direction = direction

    def __str__(self):
        direction = '/' if isinstance(self.direction, Right) else '\\'
        return f"{self.res} {direction} {self.arg}"

    def agrees_with(self, other):
        if isinstance(other, ComplexSyntacticType):
            return (self.direction == other.direction and
                    self.res.agrees_with(other.res) and
                    self.arg.agrees_with(other.arg))
        elif isinstance(other, PrimitiveSyntacticType):
            return False

class PrimitiveSyntacticType(SyntacticType):
    def __init__(self, name: str, features: List[str] = None):
        self.name = name
        self.features = features or []

    def agrees_with(self, other):
        if isinstance(other, PrimitiveSyntacticType):
            return self.name == other.name and all(feature in other.features for feature in self.features)
        return False

    def __call__(self, *features_: str):
        return PrimitiveSyntacticType(self.name, self.features + list(features_))

    def __str__(self):
        if self.features:
            return f"{self.name}({','.join(self.features)})"
        return self.name


class Category:
    def __init__(self, syntactic_type:SyntacticType, logical_form:LambdaTerm):
        self.syntactic_type = syntactic_type
        self.logical_form = logical_form

    def __repr__(self):
        return f"Category({self.syntactic_type}, {self.logical_form})"

def applies_to(p, q):
    if isinstance(p, PrimitiveSyntacticType) and isinstance(q, PrimitiveSyntacticType):
        return p.name == q.name and all(feature in q.features for feature in p.features)
    elif isinstance(p, PrimitiveSyntacticType) and isinstance(q, ComplexSyntacticType):
        return False
    elif isinstance(p, ComplexSyntacticType) and isinstance(q, PrimitiveSyntacticType):
        return False
    elif isinstance(p, ComplexSyntacticType) and isinstance(q, ComplexSyntacticType):
        return (p.direction == q.direction and
                p.res.agrees_with(q.res) and
                p.arg.agrees_with(q.arg))
    elif isinstance(c1, Category) and isinstance(c2, Category):
        return (agrees(c1.syntactic_type, c2.syntactic_type) and
                lambda_reduce(c1.logical_form) == lambda_reduce(c2.logical_form))
    elif isinstance(c1, Category) and isinstance(c2, ComplexSyntacticType):
        return False
    elif isinstance(c1, ComplexSyntacticType) and isinstance(c2, Category):
        return False
    else:
        return False

def primitive_syntactic_type(*names):
    def constructor(name):
        return PrimitiveSyntacticType(name, [])

    def def_builder2(names, constructor):
        clean_names = [name.split(".")[-1] for name in names]
        return [
            constructor(clean_name)
            for name, clean_name in zip(names, clean_names)
        ]

    return def_builder2(names, constructor)


class LexicalEntry:
    def __init__(self, lexeme, cat):
        self.lexeme = lexeme
        self.cat = cat

def LexicalEntry(lexeme, syn_type, lf):
    return LexicalEntry(lexeme, Category(syn_type, lf))

def lexeme(lexical_entry):
    return lexical_entry.lexeme

def category(lexical_entry):
    return lexical_entry.cat

class Lexicon:
    def __init__(self, lexical_entries):
        self.lexical_entries = lexical_entries

def lexical_entries(lexicon):
    return lexicon.lexical_entries

def merge(*lexicons):
    merged_entries = set()
    for lexicon in lexicons:
        merged_entries.update(lexical_entries(lexicon))
    return Lexicon(list(merged_entries))

class CombinatoryCategorialGrammar:
    def __init__(self, lexicon, type_shifting_rules):
        self.lexicon = lexicon
        self.type_shifting_rules = type_shifting_rules

def lexicon(g):
    return g.lexicon

def type_shifting_rules(g):
    return g.type_shifting_rules

def type_shifted_lexical_entries(g):
    result = list(lexical_entries(lexicon(g)))
    for entry in lexical_entries(lexicon(g)):
        new_categories = type_shifting_rules(g).get(lexeme(entry), [])
        for new_category in new_categories:
            result.append(LexicalEntry(lexeme(entry), new_category))
    return result


class LexicalEntry:
    def __init__(self, lexeme, cat):
        self.lexeme = lexeme
        self.cat = cat

def LexicalEntry(lexeme, syn_type, lf):
    return LexicalEntry(lexeme, Category(syn_type, lf))

def lexeme(lexical_entry):
    return lexical_entry.lexeme

def category(lexical_entry):
    return lexical_entry.cat

class Lexicon:
    def __init__(self, lexical_entries):
        self.lexical_entries = lexical_entries

    def lexical_entries(self):
        return self.lexical_entries

    def iterate(self, state=None):
        return iter(self.lexical_entries)

    def merge(*lexicons):
        merged_entries = set()
        for lexicon in lexicons:
            merged_entries.update(set(lexicon.lexical_entries))
        return Lexicon(list(merged_entries))

class CombinatoryCategorialGrammar:
    def __init__(self, lexicon, type_shifting_rules):
        self.lexicon = lexicon
        self.type_shifting_rules = type_shifting_rules

    def lexicon(self):
        return self.lexicon

    def type_shifting_rules(self):
        return self.type_shifting_rules

    def type_shifted_lexical_entries(self):
        result = []
        for entry in self.lexicon.lexical_entries:
            for new_category in self.type_shifting_rules.get(entry.lexeme, []):
                result.append(LexicalEntry(entry.lexeme, new_category))
        return result

class LexicalEntry:
    def __init__(self, lexeme, cat):
        self.lexeme = lexeme
        self.cat = cat

    def __str__(self):
        return f"LexicalEntry: {self.lexeme}: {self.cat}"

    @classmethod
    def from_syn_type(cls, lexeme, syn_type, lf):
        return cls(lexeme, Category(syn_type, lf))


def lexeme(lexical_entry):
    return lexical_entry.lexeme

def category(lexical_entry):
    return lexical_entry.cat

class Lexicon:
    def __init__(self, lexical_entries):
        self.lexical_entries = lexical_entries

    def __str__(self):
        entries_str = '\n'.join(str(entry) for entry in self.lexical_entries)
        return f"Lexicon entries:\n{entries_str}"

def merge(*lexicons):
    merged_entries = set()
    for lexicon in lexicons:
        merged_entries.update(lexical_entries(lexicon))
    return Lexicon(list(merged_entries))

class CombinatoryCategorialGrammar:
    def __init__(self, lexicon, type_shifting_rules):
        self.lexicon = lexicon
        self.type_shifting_rules = type_shifting_rules

def lexicon(g):
    return g.lexicon

def type_shifting_rules(g):
    return g.type_shifting_rules

def type_shifted_lexical_entries(g):
    lex = lexicon(g)
    result = lex.lexical_entries  # Remove the method call
    for entry in lex.lexical_entries:    # Call as an attribute
        new_categories = g.type_shifting_rules.get(lexeme(entry), [])
        # Process new categories as needed
    return result




def simplify(term):
    term_vars = all_vars(term)
    simplified_vars = set(map(lambda i: Variable('a' + str(i)), range(26))) - term_vars
    simplified = reduce(lambda term, v: rename_var(term, v, simplified_vars.pop()),
                             filter(lambda v: str(v).startswith('#'), term_vars),
                             init=term)
    return simplified



##########  This part is not functional yet ############


def Apply(left, right, direction):
    operator, operand = (left, right) if isinstance(direction, Right) else (right, left)
    syntactic_type_combinator = Right if isinstance(direction, Right) else Left

#    if isinstance(operator.syntactic_type, ComplexSyntacticType) and \
#       agrees(operator.syntactic_type.arg, operand.syntactic_type):
    return Category((operator.syntactic_type.res), simplify(lambda_reduce(apply(operator.logical_form, operand.logical_form))))


def Compose(left, right, direction):
    operator, operand = (left, right) if isinstance(direction, Right) else (right, left)
    syntactic_type_combinator = "/" if isinstance(direction, Right) else "\\"

#    if isinstance(operator.syntactic_type, ComplexSyntacticType) and \
#       isinstance(operand.syntactic_type, ComplexSyntacticType) and \
#       agrees(operator.syntactic_type.arg, operand.syntactic_type.res):
    return Category(syntactic_type_combinator(operator.syntactic_type.res, operand.syntactic_type.arg),
                        simplify(Compose(operator.logical_form, operand.logical_form)))



