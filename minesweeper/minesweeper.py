import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        return {}

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return {}

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # if cell is a mine -> remove it from the sentence and reduce the count
        if cell in self.cells:
            self.cells.remove(cell)
            self.count-=1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # if cell is safe -> remove it from sentence but not update the count
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        def infer_sentence(sentence1, sentence2):
            """Helper function to get inferred sentence using subset method 
                return None if new sentence cannot be inferred"""
            if sentence1.cells > sentence2.cells:
                inferred_set = sentence1.cells - sentence2.cells
                inferred_count = sentence1.count - sentence2.count
                inferred_sentence = Sentence(inferred_set, inferred_count)
                if len(inferred_set) > 0:
                    return inferred_sentence   
                else:
                    return None
            return None
        
        # 1 - Mark moves made as safe
        self.moves_made.add(cell)
        self.mark_safe(cell)
        
        # 2 - Make new sentence to AI's knowledge base
        row, col = cell
        cell_set = set()
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                # calculate nearby coordinates and check coordinates inbound
                if i>=0 and i<self.height and j>=0 and j<self.width:
                    if i == row and j == col:
                        continue
                    # only add cells with unknown state
                    if (i,j) not in self.mines and (i,j) not in self.safes and (i,j) not in self.moves_made:
                        cell_set.add((i,j))
                        
                    if (i, j) in self.mines:
                        # reduce mine count if a mine cell is found
                        count-=1
        # only add meaningful sentence (non-empty sentences)
        if len(cell_set)>0:
            new_sentence = Sentence(cells=cell_set, count=count)
            self.knowledge.append(new_sentence)
        
        # 3 - Infer new sentence
        #remove empty sentence before inferring
        for sentence in self.knowledge:
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence) 
        while True:
            # while loop to keep infer until no new sentences is created
            inferences = list()
                        
            # infer from sentences using subset method
            for i in range(len(self.knowledge)):
                for j in range(i+1, len(self.knowledge)):
                    # skip infer from same sentences
                    if self.knowledge[i] == self.knowledge[j]: continue
                    # skip infer from empty sentences
                    if len(self.knowledge[i].cells)==0 or len(self.knowledge[j].cells)==0:
                        continue
                    
                    # get the inferred sentence
                    # consider both case where sentence at i is a subset or a superset
                    inferred_sentence1 = infer_sentence(self.knowledge[i], self.knowledge[j])
                    inferred_sentence2 = infer_sentence(self.knowledge[j], self.knowledge[i])
                    # add inferred sentence to list, only add sentence that are not in knowledge base or already inferred
                    if (inferred_sentence1 is not None) and (inferred_sentence1 not in self.knowledge) and (inferred_sentence1 not in inferences):
                        inferences.append(inferred_sentence1)
                    elif (inferred_sentence2 is not None) and (inferred_sentence2 not in self.knowledge) and (inferred_sentence2 not in inferences):
                        inferences.append(inferred_sentence2)
                            
            # add inferred sentences to knowledge
            for sentence in inferences:
                self.knowledge.append(sentence)
            # stop loop when no new sentences are inferred
            if len(inferences) == 0:
                break
                            
        # 4 - Mark cells as safe or mines from inferred sentence
        safe_cells = set()
        mine_cells = set()
        for sentence in self.knowledge:
            for cell in sentence.known_safes():
                safe_cells.add(cell)
            for cell in sentence.known_mines():
                mine_cells.add(cell)  
        [self.mark_safe(cell) for cell in safe_cells]
        [self.mark_mine(cell) for cell in mine_cells]
        
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        # find a safe move that has not been made
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
            
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        # get list of possible moves
        random_list = list()
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.mines and (i,j) not in self.moves_made:
                    random_list.append((i, j))
        
        # if no possible move is found, return None
        if len(random_list) == 0:
            return None
        
        # return a random move from the list
        return random.choice(random_list)
            
