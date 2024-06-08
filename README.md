# Formal Axioms for Libertarian Property Theory

This repository contains a formal axiomatic treatment of libertarian property values using a variant of the TPTP (Thousands of Problems for Theorem Provers) syntax for higher-order logic (HOL). The file provides a set of axioms and theorems intended to capture the principles underlying libertarian property theory, including concepts such as ownership, actions, time, and deontic logic (obligations, permissions, and prohibitions).

## Syntax and Structure

The file uses a variant of the TPTP syntax designed for higher-order logic (THF format). In this format, we define types, functions, and logical statements (axioms and theorems) to express logical relationships.

Key elements of the syntax include:
- `thf(type, type, name: definition)`: Declares a new type or function.
- `thf(name, axiom, formula)`: Declares an axiom using a logical formula.
- Variables are denoted by uppercase letters, and types/functions are specified using `$i` for individuals and `$o` for truth values.

## Key Concepts

- **Time**: Defined as a type with a strict total ordering.
- **Objects, Persons, Actions**: Basic entities with time intervals.
- **Ownership and Use**: Relations capturing the ownership and use of objects by persons.
- **Deontic Logic**: Axioms governing obligations, permissions, and prohibitions related to actions and ownership.

## Example Axioms

- **Time is a strict total order**:
  ```prolog
  thf(time_strict_total_order, axiom, 
      ![T1: $i, T2: $i, T3: $i] : (
          (time(T1) & time(T2) & time(T3)) => 
          ((before(T1, T1) => $false) &                    % Irreflexivity
           ((before(T1, T2) & before(T2, T3)) => before(T1, T3)) & % Transitivity
           ((before(T1, T2) | before(T2, T1) | (T1 = T2))) % Totality
      ))).
  ```

- **Self-ownership Axiom**:
  ```prolog
  thf(self_ownership_axiom, axiom, 
      ! [P: $i, P2:$i, T1: $i, T2: $i] : (person(P, T1, T2) => ?[H:$i] : (owns(P, P, P2, H, T1, T2)))).
  ```

- **Non-Aggression Principle (NAP)**:
  ```prolog
  thf(nap, axiom, 
      ![P1: $i, P2: $i, O: $i, H:$i, U: $i, T1: $i, T2: $i] : (
          ((P1 != P2) & owns(P1, O, P2, H, T1, T2) & ~allow(P1, O, P2, U, T1, T2)) => 
          ~ permit(^ [X: $i] : use(P2, O, P2, U, T1, T2))
  )).
  ```

## Downloading and Using Leo-III

Leo-III is an automated theorem prover for higher-order logic. To use this file with Leo-III, follow these steps:

1. Download Leo-III from the [official website](https://github.com/leoprover/leo3).
2. Install Leo-III by following the instructions provided on the website.
3. Run Leo-III with the file to verify and explore the axioms.

## Suggested Additional Axioms/Theorems

While the current set of axioms provides a foundational treatment of libertarian property theory, additional axioms and theorems could be considered to further enrich the theory:

- **Trade**: Axioms governing the transfer of ownership between persons.
- **Joint Ownership**: Axioms and theorem regarding use and ownership of property owned by more than one person.

These additions can help address more complex scenarios and enhance the robustness of the formal theory.

## Questions or Contributions

For any questions or contributions, please feel free to create an issue or submit a pull request.
