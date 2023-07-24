moves = (
    bytes([2, 0, 3, 1, 6, 7, 8, 9, 10, 11, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19, 20]) + bytes(235),
    bytes([0, 1, 17, 11, 12, 4, 2, 7, 8, 9, 10, 18, 13, 5, 3, 15, 16, 19, 14, 6, 20]) + bytes(235),
    bytes([0, 5, 2, 13, 4, 19, 14, 6, 3, 9, 10, 11, 12, 20, 15, 7, 1, 17, 18, 16, 8]) + bytes(235),
    bytes([1, 3, 0, 2, 10, 11, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18, 19, 20]) + bytes(235),
    bytes([0, 1, 6, 14, 5, 13, 19, 7, 8, 9, 10, 3, 4, 12, 18, 15, 16, 2, 11, 17, 20]) + bytes(235),
    bytes([0, 16, 2, 8, 4, 1, 7, 15, 20, 9, 10, 11, 12, 3, 6, 14, 19, 17, 18, 5, 13]) + bytes(235),
)


def build_distances():
    solved = bytes(range(21))
    distances = {}
    visited = {solved}
    todo = [solved]

    for i in range(15):
        distances[i] = len(todo)
        cubes = todo
        todo = []
        for cube in cubes:
            for move in moves:
                moved = cube.translate(move)
                if moved not in visited:
                    visited.add(moved)
                    todo.append(moved)

    return distances


def build_lookup_table():
    solved = bytes(range(21))
    lookup = {solved: None}
    todo = [solved]

    for _ in range(15):
        cubes = todo
        todo = []
        for cube in cubes:
            for move in moves:
                moved = cube.translate(move)
                if moved not in lookup:
                    lookup[moved] = move
                    todo.append(moved)

    return lookup
