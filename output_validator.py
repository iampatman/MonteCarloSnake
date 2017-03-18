#!/usr/local/bin/python3

import sys

file_path = sys.argv[1]

number_of_rows = None
number_of_columns = None
chain_values = []
coordinates_and_values = []
grid = dict([])


def get_below_location(row, column):
    return [(row + 1) % number_of_rows, column]


def get_right_location(row, column):
    return [row, (column + 1) % number_of_columns]


def calculate_reward():
    node_count = 0
    for row in grid:
        for column in grid[row]:
            node_count += 1

    if node_count < len(chain_values):
        return -1 * float('inf')

    coordinate_tuples = set([])
    for coordinate_and_value in coordinates_and_values:
        t = (coordinate_and_value[0], coordinate_and_value[1])
        assert t not in coordinate_tuples
        coordinate_tuples |= {t}

    output = 0
    for row in range(0, number_of_rows):
        for column in range(0, number_of_columns):
            this_value = 0
            if row in grid and column in grid[row]:
                this_value = grid[row][column]

            if this_value == 0:
                continue

            for neighbour in [get_right_location(row, column), get_below_location(row, column)]:
                [row_neighbour, column_neighbour] = neighbour
                neighbour_value = 0
                if row_neighbour in grid and column_neighbour in grid[row_neighbour]:
                    neighbour_value = grid[row_neighbour][column_neighbour]
                output -= this_value * neighbour_value

    return output


def run(file_path):
    global number_of_rows
    global number_of_columns
    global chain_values
    global grid
    global coordinates_and_values
    lines = []
    with open(file_path, 'r') as f:
        lines_raw = f.readlines()
        for line_raw in lines_raw:
            line = line_raw.strip()
            if line:
                lines += [line]
    assert len(lines) >= 3

    problem_statement_line = lines[0]
    problem_statement_chunks = problem_statement_line.split()
    assert len(problem_statement_chunks) >= 3
    [number_of_rows, number_of_columns, chain_values] = [int(problem_statement_chunks[0]),
                                                         int(problem_statement_chunks[1]),
                                                         [int(el) for el in problem_statement_chunks[2:]]]

    for line_idx in range(1, len(lines) - 1):
        line = lines[line_idx]
        assert 3 == len(line.split())
        [row, column, value] = [int(el) for el in line.split()]
        coordinates_and_values += [[row, column, value]]
        assert value == chain_values[len(coordinates_and_values) - 1]
        if row not in grid:
            grid[row] = dict([])
        grid[row][column] = value

    if lines[-1].lower() == '-inf':
        score_expected = -1 * float('inf')
    else:
        score_expected = int(lines[-1])
    score_actual = calculate_reward()
    print('score_actual =', score_actual)
    assert score_expected == score_actual


run(file_path)
print(file_path + ' is valid')
