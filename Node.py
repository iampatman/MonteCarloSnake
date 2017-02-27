import copy
import math
from numpy import random


class Node(object):
    def __init__(self, parent, grid, x, y, s, level=0):
        self.parent_node = parent
        self.next_steps = []
        self.rewards = 0
        self.plays = 0
        self.s = s
        self.current_x = x
        self.current_y = y
        self.a = grid
        self.best_final_node = None
        self.best_final_reward = int(0)
        self.level = level

    def init_next_moves(self):
        moves = self.find_neighbors(grid=self.a, x=self.current_x, y=self.current_y)
        if len(self.s) == 0:
            print ("%s" % self.s)
            for i in range(len(self.a)):
                print self.a[i]
        for move in moves:
            b = self.cloneGrid()
            x1 = move['x']
            y1 = move['y']
            if b[x1][y1] == 2:
                b[x1][y1] = self.s[0]
                next_node = Node(self, b, x1, y1, copy.deepcopy(self.s[1:]))
                self.next_steps.append(next_node)

    def next_move(self):
        if len(self.s) == 0:
            return None
        if len(self.next_steps) == 0:
            self.init_next_moves()
        if len(self.next_steps) == 0:
            print "No next move"
            print "X=%d Y=%d" % (self.current_x, self.current_y)
            self.print_out()
            return None
        discovered_steps = filter(lambda st: st.plays > 0, self.next_steps)
        not_discovered_steps = [step for step in self.next_steps if step not in discovered_steps]
        chance = random.uniform(low=0, high=100) if len(discovered_steps) > 0 else 0
        next_step = None
        if (chance > 10 or len(not_discovered_steps) == 0) and len(discovered_steps) > 0:
            next_step = max(discovered_steps, key=lambda node: node.confidence_interval())
        else:
            if len(not_discovered_steps) > 0:
                chance = random.uniform(0, len(not_discovered_steps) + 5)
                index = math.trunc(chance) % (len(not_discovered_steps))
                next_step = not_discovered_steps[index]
        return next_step

    def calculate_additional_reward(self, grid, x, y):
        moves = self.find_neighbors(grid, x, y)
        rewards = 0
        for move in moves:
            x1 = move['x']
            y1 = move['y']
            sub_reward = 0
            if grid[x1][y1] != 2:
                sub_reward += grid[x][y] * grid[x1][y1]
            rewards += sub_reward
        return rewards * -1

    def simulate(self, depth, randomly = False):
        # rewards = math.trunc(random.uniform(1, 10))
        count_steps = 2560 - len(self.s)
        depth = len(self.s) if depth == -1 else min([depth, len(self.s)])
        s = self.s[:depth]
        current_board = self.cloneGrid()
        rewards = 0
        current_x = self.current_x
        current_y = self.current_y
        while len(s) > 0:
            moves = self.find_neighbors(grid=current_board, x=current_x, y=current_y)
            next_boards = list()
            for move in moves:
                b = copy.deepcopy(current_board)
                x1 = move['x']
                y1 = move['y']
                if b[x1][y1] == 2:
                    b[x1][y1] = s[0]
                    sub_reward = self.calculate_additional_reward(b, x1, y1)
                    next_boards.append({'x': x1, 'y': y1, 'rewards': sub_reward})

            if len(next_boards) == 0:
                print("Deadend")
                break
            else:
                count_steps += 1
            if randomly is True:
                index = math.trunc(random.uniform(0, len(next_boards) + 2)) % len(next_boards)
                next_move = next_boards[index]
            else:
                next_move = max(next_boards, key=lambda b: b['rewards'])

            current_x = next_move['x']
            current_y = next_move['y']
            current_board[current_x][current_y] = s[0]
            rewards += next_move['rewards']
            s = s[1:]
        if rewards >= self.best_final_reward and len(s) == 0 and depth == len(self.s):
            print ("Found something")
            self.best_final_node = Node(None, current_board, current_x, current_y, [])
            self.best_final_reward = rewards
        print ("steps: %d" % count_steps)
        return rewards


    def confidence_interval(self):
        if self.plays == 0 and self.parent_node is not None:
            return 0
        ub = self.rewards + math.sqrt(2 * math.log10(self.plays) / self.parent_node.plays)
        return ub

    def cloneGrid(self):
        return copy.deepcopy(self.a)

    def find_neighbors(self, grid, x, y):
        dx = [1, -1, 0, 0]
        dy = [0, 0, -1, 1]
        moves = list()
        size = len(grid)
        for i in range(4):
            x1 = x + dx[i]
            x1 = x1 % size if x1 >= 0 else x1 + size
            y1 = y + dy[i]
            y1 = y1 % size if y1 >= 0 else y1 + size
            moves.append({'x': x1, 'y': y1})
        return moves

    def print_out(self):
        for i in range(len(self.a)):
            print(self.a[i])
        print self.best_final_reward


def hash(self):
    return ""


def print_out(self):
    print(self.a)


def main():
    size = 3
    init_board = [[2 for x in range(size)] for y in range(size)]
    s = [1, 1, 0, 1, 1]
    init_board[1][1] = s[0]
    init_board[1][0] = s[1]
    init_node = Node(None, init_board, 1, 0, s[2:])
    init_node.init_next_moves()


if __name__ == '__main__':
    main()
