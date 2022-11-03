from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # or Knight or Knave, not both
    And(Or(AKnight,AKnave), Not(And(AKnight,AKnave))),

    # if A is Knight => is true
    Implication(AKnight, And(AKnight,AKnave)),
    # if A is Knave => is false
    Implication(AKnave, Not(And(AKnight,AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # or A is Knight or A is Knave, not both
    And(Or(AKnight,AKnave), Not(And(AKnight,AKnave))),
    #  or B is Knight or B is Knave, not both
    And(Or(BKnight,BKnave), Not(And(BKnight,BKnave))),

    # if A is Knight => is true
    Implication(AKnight, And(AKnave,BKnave)),
    # if A is Knave => is false
    Implication(AKnave, Not(And(AKnave,BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # or A is Knight or A is Knave, not both
    And(Or(AKnight,AKnave), Not(And(AKnight,AKnave))),
    #  or B is Knight or B is Knave, not both
    And(Or(BKnight,BKnave), Not(And(BKnight,BKnave))),

    # if A is Knight => is true
    Implication(AKnight, Or(And(AKnight,BKnight), And(AKnave,BKnave))),
    # if A is Knave => is false
    Implication(AKnave, Not(Or(And(AKnight,BKnight), And(AKnave,BKnave)))),

    # if B is Knight => is true
    Implication(BKnight, Or(And(AKnight,BKnave), And(AKnave,BKnight))),
    # if B is Knave => is false
    Implication(BKnave, Not(Or(And(AKnight,BKnave), And(AKnave,BKnight))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # or A is Knight or A is Knave, not both
    And(Or(AKnight,AKnave), Not(And(AKnight,AKnave))),
    #  or B is Knight or B is Knave, not both
    And(Or(BKnight,BKnave), Not(And(BKnight,BKnave))),
    #  or C is Knight or C is Knave, not both
    And(Or(CKnight,CKnave), Not(And(CKnight,CKnave))),

    # if B is Knight => is true => C is Knave and -v
    Implication(BKnight, CKnave),
                                                    # A said 'I am a knave'
    Implication(BKnight, And(
                Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))),
    # if B is Knave => is false => C is Knight and -v
    Implication(BKnave, Not(CKnave)),
                                                    # A said 'I am a knight'
    Implication(BKnight, And(
                Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))),

    # if C is Knight => is true
    Implication(CKnight, AKnight),
    # if C is Knave => is false
    Implication(CKnave, AKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
