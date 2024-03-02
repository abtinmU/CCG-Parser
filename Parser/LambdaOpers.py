import Utils
import LambdaUtils
import ModalLogic
import ClassifyVars

# α-conversion

# def alpha_convert(abs, new_var):
#     if isinstance(new_var, Variable):
#         if (   (new_var not in free_vars(abs)) and (new_var not in bound_vars(abs))   ):
#             return rename_var(abs, abs.var, new_var)
#         else:
#             raise ValueError(f"Invalid α-conversion: {new_var} is free or bound in {abs}")
#
#     else:
#       alpha_convert(abs, Variable(new_var))

def alpha_convert(abs, new_var):
    if isinstance(new_var, Variable):
        if new_var not in free_vars(abs) and new_var not in bound_vars(abs):
            return rename_var(abs, abs.var, new_var)
        else:
            raise ValueError(f"Invalid α-conversion: {new_var} is free or bound in {abs}")
    else:
        return alpha_convert(abs, Variable(new_var))


# α-equivalence

def alpha_equivalent(term1, term2):
      if isinstance(term1, Identifier) and isinstance(term2, Identifier):
          return term1 == term2

      elif isinstance(term1, Abstraction) and isinstance(term2, Abstraction):
          new_arg = gen_new_var(term1, term2)
          return alpha_equivalent((alpha_convert(term1, new_arg)).body, (alpha_convert(term2, new_arg)).body)

      elif isinstance(term1, Application) and isinstance(term2, Application):
          return alpha_equivalent(term1.operator, term2.operator) & alpha_equivalent(term1.operand, term2.operand)

      elif isinstance(term1, Variable) and isinstance(term2, Variable):
          stack = [(term1, term2)]
          bindings1 = {}
          bindings2 = {}
          if term1 in bindings1 and term2 in bindings2:
              if bindings1[term1] != bindings2[term2]:
                  return True
          else:
              if term1.name != term2.name:
                  return False

      elif isinstance(term1, Predicate) and isinstance(term2, Predicate):
          return term1 == term2

      elif isinstance(term1, PredicateFormula) and isinstance(term2, PredicateFormula):
          if len(term1.arguments) == len(term2.arguments) and term1.predicate== term2.predicate:
              return all(alpha_equivalent(parg, qarg) for parg, qarg in zip(term1.arguments, term2.arguments))

      elif isinstance(term1, Conjunction) and isinstance(term2, Conjunction):
          if len(term1.conjuncts) != len(term2.conjuncts):
              return False
          else:
              return all(any(alpha_equivalent(s, t) for t in term2.conjuncts) for s in term1.conjuncts) \
                    and all(any(alpha_equivalent(s, t) for t in term1.conjuncts) for s in term2.conjuncts)
      else:
            return False


# δ-reduction

def delta_reduce(term):
    if isinstance(term, Application) and isinstance(term.operator, Constant):
        constant = term.operator
        if constant.name == 'add':
            return Constant('(+ ' + str(term.operand.operator) + ' ' + str(term.operand.operand) + ')')
        elif constant.name == 'multiply':
            return Constant('(* ' + str(term.operand.operator) + ' ' + str(term.operand.operand) + ')')
        else:
            return term
    else:
        return term


# η-reduction

def is_eta(abs):
    return isinstance(abs.body, Application) and abs.body.operand == abs.var

def eta_reduce(abs):
    if is_eta(abs):
        return abs.body.operator
    else:
        return abs

# β-reduction

def beta_reduce(term):
    if isinstance(term, Application) and isinstance(term.operator, Abstraction):
        return replacement(term.operator.body, term.operator.var, term.operand)
    else:
        return term

# Normal Order

def normal_order(term):
    if isinstance(term, Application):
        operator = normal_order(term.operator)
        if isinstance(operator, Abstraction):
            operand = normal_order(term.operand)
            return normal_order(replacement(operator.body, operator.var, operand))
        else:
            return Application(operator, normal_order(term.operand))
    elif isinstance(term, Abstraction):
        return Abstraction(term.var, normal_order(term.body))
    else:
        return term


# Lambda Reduction - General


def lambda_reduce(term, prev_term=None):
    if prev_term is not None and term == prev_term:
        return term

    if isinstance(term, Application):
        new_operator = term.operator
        new_operand = term.operand
        new_operator, new_operand = chek_oper_App_or_Abs(new_operator, new_operand)

        return beta_reduce(apply(new_operator, new_operand))


    elif isinstance(term, Abstraction):
        if alpha_equivalent(term, prev_term):
            return term
        else:
            simplified = eta_reduce(term)
            if isinstance(simplified, Abstraction):
                return lambda_reduce(lambda_(simplified.var, lambda_reduce(simplified.body)), term)
                # return lambda_reduce(Abstraction(simplified.var, lambda_reduce(simplified.body)), term)
            else:
                return lambda_reduce(simplified)

            # simplified_args = [lambda_reduce(arg) for arg in term.arguments]
            # return lambda_reduce(apply(term.predicate, *simplified_args), term)

    elif isinstance(term, PredicateFormula):
        if alpha_equivalent(term, prev_term):
            term
        else:
            simplified_args = [lambda_reduce(arg) for arg in term.arguments]
            return lambda_reduce(term.predicate(*simplified_args), term)

    elif isinstance(term, Conjunction):
        simplified_conjs = [lambda_reduce(t) for t in term.conjuncts]
        return Conjunction(*simplified_conjs)

    else:
        return term
