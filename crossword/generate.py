import sys

from crossword import *
from collections import deque


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable, values in self.domains.items():
            removed_words = set()

            for word in values:
                # remove words that does not match Variable length
                if len(word) != variable.length:
                    removed_words.add(word)
            self.domains[variable] = self.domains[variable] - removed_words

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if self.crossword.overlaps[x, y] is not None:
            x_index, y_index = self.crossword.overlaps[x, y]
            removed_words = set()

            # check each pair of word in x and y, remove word if there is no corresponding word in y
            for x_val in self.domains[x]:
                have_corresponding = False

                # check if corresponding word in y available
                for y_val in self.domains[y]:
                    if x_val[x_index] == y_val[y_index]:
                        have_corresponding = True

                if not have_corresponding:
                    removed_words.add(x_val)
            self.domains[x] = self.domains[x] - removed_words

            # modification made if there are more than 0 word removed from domain
            return len(removed_words) > 0

        # no arc consistency is enforced when x and y don't overlap
        return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = deque()
            # if arcs is None, begin with list of all arcs
            variables = list(self.domains.keys())
            # generate list of arcs from each variable to its neighbors
            for variable in variables:
                for neighbor in self.crossword.neighbors(variable):
                    arcs.append((variable, neighbor))
        else:
            arcs = deque(arcs)

        while len(arcs) > 0:
            x, y = arcs.popleft()
            if self.revise(x, y):
                # if no value left in domain -> problem is unsolvable
                if len(self.domains[x]) == 0:
                    return False

                # add neighbors that are not y to enforce consistency with new value of x
                for neighbor in self.crossword.neighbors(x):
                    if neighbor == y:
                        continue
                    # only add if pair is not already in arcs
                    if (x, neighbor) not in arcs:
                        arcs.append((x, neighbor))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # assignment done when there is assigned value for all variables in domain
        return len(assignment) == len(self.domains)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        assigned_values = set()
        for variable, value in assignment.items():
            # check if any values were previously assigned
            if value in assigned_values:
                return False
            # check if value is correct length
            if len(value) != variable.length:
                return False

            # check if there is conflict with neighbors:
            for neighbor in self.crossword.neighbors(variable):
                if neighbor in assignment:
                    x_index, y_index = self.crossword.overlaps[variable, neighbor]
                    # if there is conflict, return False
                    if variable[x_index] != variable[y_index]:
                        return False
            # keep track of assigned values
            assigned_values.add(value)

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # instantiate dictionary of values and its n value
        constraining_value = {key: 0 for key in self.domains[var]}

        # update constraining value
        for neighbor in self.crossword.neighbors(var):
            if neighbor in assignment:
                continue  # skip neighbors with assigned value

            for val in self.domains[var]:
                for neighbor_val in self.domains[neighbor]:
                    # if value of variable is also in neighbor -> increase constraining value
                    if val == neighbor_val:
                        constraining_value[val] += 1

                    # if value cause conflict to another value in neighbor -> increase constraining value
                    x_index, y_index = self.crossword.overlaps[var, neighbor]
                    if val[x_index] != neighbor_val[y_index]:
                        constraining_value[val] += 1

        # get ordered list based on heuristics
        ordered_list = [value for value, heuristic in sorted(constraining_value.items(), key=lambda item: item[1])]
        return ordered_list

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        variables = list(self.domains.keys())

        # filter out variables that have been assigned
        variables = [var for var in variables if var not in assignment]

        # find list of variables with min number of domain
        least_domains = []
        min_no_domains = 99999999999999
        for var in variables:
            if len(self.domains[var]) < min_no_domains:
                # if variable with lower number of domains is found -> update number of min domains and list
                min_no_domains = len(self.domains[var])
                least_domains = [var]
            elif len(self.domains[var]) == min_no_domains:
                # if another variable have the same number of domain -> update list
                least_domains.append(var)

        # find list of variables with max number of degree
        highest_degree = None
        max_degree = 0
        for var in least_domains:
            degree = len(self.crossword.neighbors(var))
            if degree > max_degree:
                max_degree = degree
                highest_degree = var
        return highest_degree

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # base case, return assignment when it is complete
        if self.assignment_complete(assignment=assignment):
            return assignment

        variable = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(variable, assignment):
            # create a copy for backtracking
            new_assignment = assignment.copy()
            new_assignment[variable] = value
            
            # recursive call
            result = self.backtrack(new_assignment)
            # return valid result
            if result is not None:
                return result

        # return None for failed cases 
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
