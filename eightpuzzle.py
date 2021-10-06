import copy
import time
from queue import PriorityQueue

class Puzzle:
    """A sliding-block puzzle."""
    g_score = 0
    h_score = 0
    f_score = 0
    last_move = ""

    def __init__(self, grid):
        """Instances differ by their number configurations."""
        self.grid = copy.deepcopy(grid) # No aliasing!
    
    def display(self):
        """Print the puzzle."""
        for row in self.grid:
            for number in row:
                print(number, end="")
            print()
        print()

    def moves(self):
        """Return a list of possible moves given the current configuration."""
        moves = []
        i = ()
        for row in self.grid:
            for number in row:
                if number == " ":
                    i = (self.grid.index(row), self.grid[self.grid.index(row)].index(" "))

        if i[0] == 0:
            moves.append("S")
        if i[0] == 1:
            moves.append("N")
            moves.append("S")
        if i[0] == 2:
            moves.append("N")
        if i[1] == 0:
            moves.append("E")
        if i[1] == 1:
            moves.append("W")
            moves.append("E")
        if i[1] == 2:
            moves.append("W")

        return moves

    def neighbor(self, move):
        """Return a Puzzle instance like this one but with one move made."""
        puzzle = self
        i = ()
        for row in puzzle.grid:
            for number in row:
                if number == " ":
                    i = (puzzle.grid.index(row), puzzle.grid[puzzle.grid.index(row)].index(" "))

        if move == "N":
            puzzle.grid[i[0]][i[1]] = puzzle.grid[i[0] - 1][i[1]]
            puzzle.grid[i[0] - 1][i[1]] = " "
        if move == "E":
            puzzle.grid[i[0]][i[1]] = puzzle.grid[i[0]][i[1] + 1]
            puzzle.grid[i[0]][i[1] + 1] = " "
        if move == "S":
            puzzle.grid[i[0]][i[1]] = puzzle.grid[i[0] + 1][i[1]]
            puzzle.grid[i[0] + 1][i[1]] = " "
        if move == "W":
            puzzle.grid[i[0]][i[1]] = puzzle.grid[i[0]][i[1] - 1]
            puzzle.grid[i[0]][i[1] - 1] = " "

        self.last_move = move
        return puzzle

    def h(self, goal):
        """Compute the distance heuristic from this instance to the goal."""
        # YOU FILL THIS IN
        h = 0
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == " ":
                    self.grid[i][j] = 0

                if self.grid[i][j] != 0:
                    x, y = divmod(self.grid[i][j], 3)
                    h += abs(x - i) + abs(y - j)

        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == 0:
                    self.grid[i][j] = " "
        self.h_score += h
        return h

    def g(self):
        self.g_score += 1

    def f(self, g_score, h_score):
        self.f_score = g_score + h_score

class Agent:
    """Knows how to solve a sliding-block puzzle with A* search."""

    def __init__(self):
        self.path = []

    def astar(self, puzzle, goal):
        """Return a list of moves to get the puzzle to match the goal."""
        # YOU FILL THIS IN
        open_list = PriorityQueue()
        open_list.put((puzzle.f_score, id(puzzle), puzzle))
        closed_list = []

        id_dictionary = {id(puzzle): id(puzzle)}
        puzzle_dictionary = {puzzle: puzzle}

        puzzle.h(goal)
        puzzle.f(puzzle.g_score, puzzle.h_score)

        i = 0

        while open_list.empty() is False:
            current_item = open_list.get(0)
            current_id = current_item[1]
            current_puzzle = current_item[2]

            if i == 0:
                id_dictionary[current_id] = current_id
                puzzle_dictionary[current_puzzle] = current_puzzle

            current_puzzle.display()
            moves_list = current_puzzle.moves()

            if current_puzzle.grid == goal.grid:
                # Find the solved puzzle item
                path = []
                moves_list = []
                i = 0
                puzzle_dictionary_key_list = list(puzzle_dictionary.keys())
                for puz in puzzle_dictionary_key_list:
                    if puz.grid == goal.grid:
                        i = puzzle_dictionary_key_list.index(puz)

                solved_puzzle = list(puzzle_dictionary.keys())[i]
                temp = solved_puzzle
                while puzzle_dictionary[temp] != puzzle:
                    if temp in puzzle_dictionary:
                        temp = puzzle_dictionary[temp]
                        path.append(temp)

                path.append(puzzle)
                path.reverse()
                path.append(solved_puzzle)

                #print(list(puzzle_dictionary.keys())[i].grid)
                #print("Last dictionary key entry is: ", list(puzzle_dictionary.keys())[-3].grid)
                #print("Last dictionary value entry is: ", list(puzzle_dictionary.values())[-3].grid)

                path.pop(0)
                for p in path:
                    moves_list.append(p.last_move)

                return moves_list

            i += 1
            for move in moves_list:
                new_puzzle = copy.deepcopy(current_puzzle)
                new_puzzle.neighbor(move)
                new_puzzle.f_score = 0
                new_puzzle.h_score = 0
                new_puzzle.g_score = i
                new_puzzle.h(goal)

                new_puzzle.f(new_puzzle.g_score, new_puzzle.h_score)
                id_dictionary[id(new_puzzle)] = current_id
                puzzle_dictionary[new_puzzle] = current_puzzle
                open_list.put((new_puzzle.f_score, id(new_puzzle), new_puzzle, move))


#old_puzzle = copy.deepcopy(current_puzzle)
#new_puzzle = Puzzle(current_puzzle.neighbor(move).grid)
#current_puzzle = old_puzzle
#print(current_puzzle.grid[0], "\n", current_puzzle.grid[1], "\n", current_puzzle.grid[2])
def main():
    """Create a puzzle, solve it with A*, and console-animate."""

    puzzle1 = Puzzle([[1, 2,  5],
                     [4, 8,  7],
                     [3, 6,' ']])
    puzzle2 = Puzzle([[1, 2, 5],
                     [3, 6, ' '],
                     [4, 8, 7]])
    puzzle3 = Puzzle([[1, 3, 2],
                     [4, 6, 5],
                     [' ', 7, 8]])
    puzzle1_start = [[1, 2, 5],
                     [4, 8, 7],
                     [3, 6, ' ']]
    puzzle2_start = [[1, 2, 5],
                     [3, 6, ' '],
                     [4, 8, 7]]
    puzzle3_start = [[1, 3, 2],
                     [4, 6, 5],
                     [' ', 7, 8]]
    puzzle_goal = [[' ', 1, 2],
                   [3, 4, 5],
                   [6, 7, 8]]

    """
    Manual Manhattan distance calculation for this instance.
    1 + 1 + 1 + 1 + 2 + 2 + 1 + 1 = 10
    """

    #moves = []
    #puzzle.display()
    #moves = puzzle.moves()

    agent = Agent()
    path = agent.astar(Puzzle(puzzle2_start), Puzzle(puzzle_goal))
    puzzle = puzzle2

    while path:
        move = path.pop(0)
        puzzle = puzzle.neighbor(move)
        time.sleep(1)
        puzzle.display()

if __name__ == '__main__':
    main()