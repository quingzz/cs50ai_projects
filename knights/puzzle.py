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
    #A's statement is true iff A is a knight
    Biconditional(And(AKnight, AKnave), AKnight),
    # problem constraint: one can only either knight or knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)))
)   

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A's statement is true iff A is knight
    Biconditional(And(AKnave, BKnave), AKnight),
    # problem constraint: one can only either knight or knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A is a knight iff the statement is true
    Biconditional(Or(And(AKnave, BKnave), And(AKnight, BKnight)), AKnight),
    # B is a knight iff the statement is true
    Biconditional(Or(And(AKnave, BKnight), And(AKnight, BKnave)), BKnight),
    
    # problem constraint: one can only either knight or knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A is knight iff either statement is right
    Biconditional(Or(AKnight, AKnave), AKnight),
    # B is a knight iff statement "C is a knave." is true
    Biconditional(CKnave, BKnight),
    # C is a knight iff statement "A is a knight." is true
    Biconditional(CKnight, AKnight),
    # statement "A said 'I am a knave'." is true if B is knight
    # the statement can be intepreted as "A saying the truth if A is a Knight" or "A tell a lie if A is a Knave"
    Implication(BKnight, Or(Biconditional(AKnave, Not(AKnave)), Biconditional(AKnight, AKnave))),
    
    # problem constraint: one can only either knight or knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave)))
    
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
