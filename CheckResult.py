import sys

INPUT_FILE_NAMES = ["test.dat"]
VALID_DATA = True


def readData(filename):
    with open(filename) as f:
        steps = list()
        first_line = f.readline()
        first_line_array = first_line.split(" ")
        n = int(first_line_array[0])
        s = [int(x) for x in first_line_array[2:] if not x.isspace()]
        line = f.readline()

        while line != "":
            data = [int(x) for x in line.split(' ')]
            steps.append(data)
            line = f.readline()
        f.close()
        return {'size': n, 's': s, 'data': steps}


def readGrid():
    with open('result.dat') as f:
        lines = f.readlines()
        n = len(lines)
        a = [y for y in range(n)]
        for index, line in enumerate(lines):
            line = line.strip().split(',')
            line = [int(ch) for ch in line]
            a[index] = line
        return {'size': n, 'data': a}


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else 'output_node_config.dat'
    result = readData(filename)
    a = result['data']
    size = result['size']
    s = result['s']
    VALID_DATA = True
    a = [[2 for x in range(size)] for y in range(size)]
    reward = 0
    for index, step in enumerate(result['data']):
        x = step[0]
        y = step[1]
        q = step[2]
        if q not in {-1, 0, 1} or q != s[index]:
            VALID_DATA = False
            break
        if a[x][y] != 2:
            VALID_DATA = False
        a[x][y] = q
    # for row in (a[i] for i in range(size)):
    #     print row
    if VALID_DATA is False:
        print "Data invalid"
    else:
        print "Reward is %d" % check_result(a, s)


def check_result(a):
    reward = 0
    size = len(a)
    count = 0
    for x in range(size):
        for y in range(size):
            if a[x][y] != 2:
                count += 1
                value = a[x][y]
                neighbors = find_neighbors(size, x, y)
                neighbors = filter(lambda k: a[k['x']][k['y']] != 2, neighbors)
                sub_total = sum([a[k['x']][k['y']] * value for k in neighbors]) * -1
                reward += sub_total
    print "Count %d" % count
    print "Rewards %d" % (reward / 2)
    return reward / 2


def find_neighbors(size, x, y):
    dx = [1, -1, 0, 0]
    dy = [0, 0, -1, 1]
    moves = list()
    for i in range(4):
        x1 = x + dx[i]
        x1 = x1 % size if x1 >= 0 else x1 + size
        y1 = y + dy[i]
        y1 = y1 % size if y1 >= 0 else y1 + size
        # if (x1 <= x and y1 <= y) or (x1 == size - 1) or y1 == size -1:
        moves.append({'x': x1, 'y': y1})
    return moves


if __name__ == '__main__':
    main()
