INPUT_FILE_NAMES = ["test.dat"]
VALID_DATA = True


def readData():
    with open('test.dat') as f:
        steps = list()
        lines = f.readline()
        n = int(lines)
        line = f.readline()
        while line != "":
            data = [int(x) for x in line.split(' ')]
            steps.append(data)
            line = f.readline()
        return {'size': n, 'data': steps}


def readGrid():
    with open('result.dat') as f:
        lines = f.readlines()
        n = len(lines)
        a = [y for y in range(n)]
        for index, line in enumerate(lines):
            line = line.strip().split(',')
            line = [int(ch)for ch in line]
            a[index] = line
        return {'size': n, 'data': a}


def main():

    result = readGrid()
    a = result['data']
    size = result['size']
    check_result(a)

    a = [[2 for x in range(size)] for y in range(size)]
    reward = 0
    for index, step in enumerate(result['data']):
        x = step[0]
        y = step[1]
        q = step[2]
        if q not in {-1, 0, 1}:
            VALID_DATA = False
            break
        if a[x][y] != 2:
            VALID_DATA = False
        a[x][y] = q
    for row in (a[i] for i in range(size)):
        print row
    for x in range(size):
        for y in range(size):
            if a[x][y] != 2:
                value = a[x][y]
                neighbors = find_neighbors(size, x, y)
                neighbors = filter(lambda k: a[k['x']][k['y']] != 2, neighbors)
                sub_total = sum([a[k['x']][k['y']] * value for k in neighbors]) * -1
                reward += sub_total
    print reward


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
    print count
    print reward/2


def find_neighbors(size, x, y):
    dx = [1, -1, 0, 0]
    dy = [0, 0, -1, 1]
    moves = list()
    for i in range(4):
        x1 = x + dx[i]
        x1 = x1 % size if x1 >= 0 else x1 + size
        y1 = y + dy[i]
        y1 = y1 % size if y1 >= 0 else y1 + size
        #if (x1 <= x and y1 <= y) or (x1 == size - 1) or y1 == size -1:
        moves.append({'x': x1, 'y': y1})
    return moves


if __name__ == '__main__':
    main()
