# CCG Semantic Parser

This repository contains my implementation of a Combinatory Categorial Grammar (CCG) semantic parser in Python. In this project, I implemented some of the interesting topics I learned in COGS543 (Computational Semantics) and COGS532 (Computational Morphology and Syntax) graduate courses. This parser combines lambda calculus, modal logic, and syntactic structures to analyze and derive the semantics of natural language sentences.

The current version is done with the general implementations, but the final CCG component still needs some modifications.

---

## Features

- **Lambda Calculus**:
  - Supports abstraction, application, and variable manipulation.
  - Implements β, η, and δ-reduction for simplifying logical forms.
- **Modal Logic**:
  - Handles conjunctions, disjunctions, negations, and quantifiers.
  - Supports modal operators like necessity (`□`) and possibility (`◇`).
- **Combinatory Categorial Grammar (CCG)**:
  - Implements syntactic types (`PrimitiveSyntacticType`, `ComplexSyntacticType`).
  - Combines syntax and semantics with categories and type-shifting rules.
- **Variable Management**:
  - Distinguishes free and bound variables in logical terms.
  - Provides utilities for α-conversion and variable renaming.

---

## Project Structure

```
CCG-Parser
├── Parser/
│   ├── ClassifyVars.py    # Handles free and bound variable classification.
│   ├── IMCCG.py           # Implements CCG constructs and syntactic types.
│   ├── LambdaUtils.py     # Defines lambda calculus operations and utilities.
│   ├── LambdaCalculus.py  # Implements reduction techniques (β, η, δ) and normal forms.
│   ├── ModalLogic.py      # Provides modal logic constructs.
│   └── Utils.py           # Contains helper functions for code generation and iteration.
└── Semantic Parser Tests.ipynb # Tests for various parser components
```
