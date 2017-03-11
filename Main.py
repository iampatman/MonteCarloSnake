from Node import Node
import CheckResult
import sys
import datetime
INPUT_FILE_NAMES = ["data_submission/L64_s02.dat"]
n = 0
TOTAL_TRIES = 1000
# data_submission/L08_s01.dat
def readData(filename):
    with open(filename) as f:
        lines = f.readlines()
        array = lines[0].strip().split(' ')
        str = list(int(ch) for ch in array)
        print str
        n = str[0]
        a = str[2:]
        f.close()
        return {'size': n, 'data': a}


def main():
    starttime =datetime.datetime.now()

    filename = "data_submission/" + sys.argv[1] if len(sys.argv) > 1 else 'data_submission/L64_s01.dat'
    result = readData(filename)
    s = result['data']
    size = result['size']
    init_board = [[2 for x in range(size)] for y in range(size)]
    print(len(s))
    init_board[1][1] = s[0]
    init_board[1][2] = s[1]
    root = Node(0, None, init_board, 1, 2, s[2:])
    # print init_node.look_ahead(init_board, s[0] * s[1] * -1, 1, 2, s[2:])
    run(root)
    for move in print_solution(root, s):
        print "%d %d %d" % (move['x'], move['y'], move['k'])
    write_to_file("output_node_config_L64_s01.dat", print_solution(root, s), size)
    endtime = datetime.datetime.now()
    print endtime-starttime
    root.best_final_node.print_out()
    CheckResult.check_result(root.best_final_node.a)



def write_to_file(filename, moves, size):
    with open(filename, 'w') as f:
        f.write('%d\n' % size)
        for move in moves:
            f.write("%d %d %d\n" % (move['x'], move['y'], move['k']))
        f.close()


def run(root):
    current_running_times = 0
    MAX_RUNNING_TIMES = 100
    while (current_running_times < MAX_RUNNING_TIMES):
        # while root.best_final_node is None:
        print ("Time: %d" % (current_running_times + 1))
        # Selection phase
        next = root.next_move()
        # tracing = [0]
        while next is not None and next.plays != 0:
            # tracing.append(next.id)
            next = next.next_move()
        # Expansion
        # print ("Tracing ids:" + str(tracing))
        if next is not None:
            current_node = next
            # SIMULATION
            reward = current_node.simulate(-1)
            print ("Rewards: %d" % reward)
            current_node.rewards = reward
            current_node.plays = 1
            # BACK PROPAGATING
            while current_node.parent_node is not None:
                parent = current_node.parent_node
                parent.rewards += reward
                parent.plays += 1
                if current_node.best_final_node is not None and current_node.best_final_reward >= parent.best_final_reward:
                    parent.best_final_node = current_node.best_final_node
                    parent.best_next_node_to_result = current_node
                    parent.best_final_reward = current_node.best_final_reward
                current_node = parent
        current_running_times += 1
        print ("==================")


def print_solution(root, s):
    moves = [{'x': 1, 'y': 1, 'k': s[0]}, {'x': 1, 'y': 2, 'k': s[1]}]
    current_node = root
    index = 1
    while current_node.best_next_node_to_result is not None:
        current_node = current_node.best_next_node_to_result
        index += 1
        moves.append({'x': current_node.current_x, 'y': current_node.current_y, 'k': s[index]})
    moves_to_result = current_node.moves_to_result
    for move in moves_to_result:
        index += 1
        moves.append({'x': move['x'], 'y': move['y'], 'k': s[index]})
    return moves


def find_last_solution(root):
    current_node = root
    while len(current_node.next_steps) > 0:
        next_move = max(current_node.next_steps, key=lambda node: node.confidence_interval())
        current_node = next_move

    print ("Len of s: %d" % (len(current_node.s)))
    current_running_times = 1
    MAX_RUNNING_TIMES = 3000
    reward = 0
    while current_running_times <= MAX_RUNNING_TIMES:
        print(current_running_times)
        reward = max(reward, current_node.simulate(-1, True))
        current_running_times += 1
    print ("reward found by random")
    return reward


if __name__ == '__main__':
    main()
