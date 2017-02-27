from Node import Node
import CheckResult

INPUT_FILE_NAMES = ["test.dat"]
n = 0
TOTAL_TRIES = 1000


def readData():
    with open('data_submission/L64_s02.dat') as f:
        lines = f.readlines()
        array = lines[0].strip().split(' ')
        str = list(int(ch) for ch in array)
        print str
        n = str[0]
        a = str[2:]
        return {'size': n, 'data': a}


def main():
    result = readData()
    s = result['data']
    size = result['size']
    # size = 5
    init_board = [[2 for x in range(size)] for y in range(size)]
    # s = [1, -1, 1, -1, 1, 1, -1, 1, 1, 1]
    print(len(s))
    init_board[1][1] = s[0]
    init_node = Node(None, init_board, 1, 1, s[1:])
    run(init_node)
    # print find_last_solution(init_node)
    init_node.best_final_node.print_out()
    CheckResult.check_result(init_node.best_final_node.a)


def run(root):
    current_running_times = 0
    MAX_RUNNING_TIMES = 4000
    # while (current_running_times < MAX_RUNNING_TIMES:
    while root.best_final_node is None:
        print ("Time: %d" % (current_running_times + 1))
        # Selection phase
        next = root.next_move()
        while next is not None and next.plays != 0:
            next = next.next_move()
        # Expansion
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
                parent.best_final_reward = current_node.best_final_reward
            current_node = parent

        current_running_times += 1
        print ("==================")


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
