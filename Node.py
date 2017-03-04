import copy
import math
import sys
from numpy import random
import CheckResult


class Node(object):
    def __init__(self, id, parent, grid, x, y, s, level=0):
        self.id = id
        self.parent_node = parent
        self.next_steps = []
        self.rewards = 0
        self.plays = 0
        self.s = s
        self.current_x = x
        self.current_y = y
        self.a = grid
        self.best_final_node = None
        self.best_final_reward = sys.maxint * -1
        self.level = level

    def init_next_moves(self):
        moves = self.find_neighbors(grid=self.a, x=self.current_x, y=self.current_y)
        if len(self.s) == 0:
            print ("%s" % self.s)
            for i in range(len(self.a)):
                print self.a[i]
        for i, move in enumerate(moves):
            b = self.cloneGrid()
            x1 = move['x']
            y1 = move['y']
            if b[x1][y1] == 2:
                b[x1][y1] = self.s[0]
                next_node = Node(self.id * 3 + i + 1, self, b, x1, y1, copy.deepcopy(self.s[1:]))
                self.next_steps.append(next_node)

    def next_move(self):
        if len(self.s) == 0:
            return None
        if len(self.next_steps) == 0:
            self.init_next_moves()
        if len(self.next_steps) == 0:
            print "No next move"
            print "X=%d Y=%d" % (self.current_x, self.current_y)
            # self.print_out()
            return None
        discovered_steps = filter(lambda st: st.plays > 0, self.next_steps)
        not_discovered_steps = [step for step in self.next_steps if step not in discovered_steps]
        chance = random.uniform(low=0, high=100) if len(discovered_steps) > 0 else 0
        next_step = None
        if (chance > 80 or len(not_discovered_steps) == 0) and len(discovered_steps) > 0:
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

    def simulate(self, depth, randomly=False):
        # rewards = math.trunc(random.uniform(1, 10))
        count_steps = 2560 - len(self.s)
        depth = len(self.s) if depth == -1 else min([depth, len(self.s)])
        s = self.s[:depth]
        current_board = self.cloneGrid()
        rewards = 0
        current_x = self.current_x
        current_y = self.current_y
        while len(s) > 0:
            lookahead_result = self.look_ahead(grid=current_board, r=0, s=s[:min(5, len(s))], x=current_x, y=current_y)
            if lookahead_result["move"] is None:
                print("Deadend")
                break
            count_steps += 1;
            next_move = lookahead_result["move"]
            current_x = next_move['x']
            current_y = next_move['y']
            current_board[current_x][current_y] = s[0]
            rewards += self.calculate_additional_reward(current_board, current_x, current_y)
            s = s[1:]

        if rewards >= self.best_final_reward and len(s) == 0 and depth == len(self.s):
            print ("Found something")
            self.best_final_node = Node(-1, None, current_board, current_x, current_y, [])
            self.best_final_reward = rewards
        print ("steps: %d" % count_steps)
        return rewards

    def confidence_interval(self):
        parent_plays = 0 if self.parent_node is None else self.parent_node.plays
        if self.plays == 0:
            return 10000000
        ub = self.rewards / self.plays + math.sqrt(2 * math.log10(parent_plays) / self.plays)
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

    def look_ahead(self, grid, r, x, y, s):
        # return reward when do a look ahead
        moves = self.find_neighbors(grid, x, y);
        max_rewards = sys.maxint * -1;
        max_move = None
        # Reach the target
        for move in moves:
            x1 = move['x']
            y1 = move['y']
            if grid[x1][y1] == 2:
                grid[x1][y1] = s[0]
                add_reward = self.calculate_additional_reward(grid, x1, y1)
                if len(s) > 1:
                    result = self.look_ahead(grid, r + add_reward, x1, y1, s[1:])
                    if result['rewards'] > max_rewards:
                        max_rewards = result['rewards']
                        max_move = move
                else:
                    if r + add_reward > max_rewards:
                        max_rewards = r + add_reward
                        max_move = move;
                grid[x1][y1] = 2
        return {'rewards': max_rewards, 'move': max_move}

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
