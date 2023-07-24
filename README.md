# pocket-cube

A Pocket Cube is a $2\times2\times2$ [Combination Puzzle](https://en.wikipedia.org/wiki/Combination_puzzle). It has 3674160 different states.

$$\frac{8!\times 3^7}{24}=7!\times3^6=3,674,160$$

We can generate all of them by representing the cube states with permutations.
The solved cube will be the identity:

```s
+-------+
|  0  1 |
|  2  3 |
+-------+-------+-------+-------+
|  4  5 |  6  7 |  8  9 | 10 11 |
| 12 13 | 14 15 | 16  . |  . 17 |
+-------+-------+-------+-------+
| 18 19 |
|  . 20 |
+-------+
```

The dots represent a fixed corner to avoid repetition. There are 24 possible orientation of the same cube.

We can define the moves as permutations:

### moves[0]

```s
+-------+
|  2  0 |
|  3  1 |
+-------+-------+-------+-------+
|  6  7 |  8  9 | 10 11 |  4  5 |
| 12 13 | 14 15 | 16  . |  . 17 |
+-------+-------+-------+-------+
| 18 19 |
|  . 20 |
+-------+
```

### moves[1]

```s
+-------+
|  0  1 |
| 17 11 |
+-------+-------+-------+-------+
| 12  4 |  2  7 |  8  9 | 10 18 |
| 13  5 |  3 15 | 16  . |  . 19 |
+-------+-------+-------+-------+
| 14  6 |
|  . 20 |
+-------+
```

### moves[2]

```s
+-------+
|  0  5 |
|  2 13 |
+-------+-------+-------+-------+
|  4 19 | 14  6 |  3  9 | 10 11 |
| 12 20 | 15  7 |  1  . |  . 17 |
+-------+-------+-------+-------+
| 18 16 |
|  .  8 |
+-------+
```

### moves[3] (inverse of moves[0])

```s
+-------+
|  1  3 |
|  0  2 |
+-------+-------+-------+-------+
| 10 11 |  4  5 |  6  7 |  8  9 |
| 12 13 | 14 15 | 16  . |  . 17 |
+-------+-------+-------+-------+
| 18 19 |
|  . 20 |
+-------+
```

### moves[4] (inverse of moves[1])

```s
+-------+
|  0  1 |
|  6 14 |
+-------+-------+-------+-------+
|  5 13 | 19  7 |  8  9 | 10  3 |
|  4 12 | 18 15 | 16  . |  .  2 |
+-------+-------+-------+-------+
| 11 17 |
|  . 20 |
+-------+
```

### moves[5] (inverse of moves[2])

```s
+-------+
|  0 16 |
|  2  8 |
+-------+-------+-------+-------+
|  4  1 |  7 15 | 20  9 | 10 11 |
| 12  3 |  6 14 | 19  . |  . 17 |
+-------+-------+-------+-------+
| 18  5 |
|  . 13 |
+-------+
```

There is a little known Python method called [`bytes.translate()`](https://docs.python.org/3/library/stdtypes.html#bytes.translate) which allows us to multiply permutations.<br>
We can define the moves as bytes objects and use them as translation tables.

```py
moves = (
    bytes([2, 0, 3, 1, 6, 7, 8, 9, 10, 11, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19, 20]) + bytes(range(21, 256)),
    bytes([0, 1, 17, 11, 12, 4, 2, 7, 8, 9, 10, 18, 13, 5, 3, 15, 16, 19, 14, 6, 20]) + bytes(range(21, 256)),
    bytes([0, 5, 2, 13, 4, 19, 14, 6, 3, 9, 10, 11, 12, 20, 15, 7, 1, 17, 18, 16, 8]) + bytes(range(21, 256)),
    bytes([1, 3, 0, 2, 10, 11, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18, 19, 20]) + bytes(range(21, 256)),
    bytes([0, 1, 6, 14, 5, 13, 19, 7, 8, 9, 10, 3, 4, 12, 18, 15, 16, 2, 11, 17, 20]) + bytes(range(21, 256)),
    bytes([0, 16, 2, 8, 4, 1, 7, 15, 20, 9, 10, 11, 12, 3, 6, 14, 19, 17, 18, 5, 13]) + bytes(range(21, 256)),
)
```

We can now generate all the pocket cube states.

```py
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
```

We can run the above function and measure how long it takes to find all the possible cube states.

```py
import time

import pocket_cube

start = time.time()
distances = pocket_cube.build_distances()
end = time.time()

for distance, count in distances.items():
    print(f'{count} pocket cubes with a solution of {distance} moves')

print(f'it took {end - start:.2f} seconds to finish')
```

```
1 pocket cubes with a solution of 0 moves
6 pocket cubes with a solution of 1 moves
27 pocket cubes with a solution of 2 moves
120 pocket cubes with a solution of 3 moves
534 pocket cubes with a solution of 4 moves
2256 pocket cubes with a solution of 5 moves
8969 pocket cubes with a solution of 6 moves
33058 pocket cubes with a solution of 7 moves
114149 pocket cubes with a solution of 8 moves
360508 pocket cubes with a solution of 9 moves
930588 pocket cubes with a solution of 10 moves
1350852 pocket cubes with a solution of 11 moves
782536 pocket cubes with a solution of 12 moves
90280 pocket cubes with a solution of 13 moves
276 pocket cubes with a solution of 14 moves
it took 7.08 seconds to finish
```

To be able to solve the cube we must store the moves in a lookup table.

```py
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
```

Any state now maps to a move that produced it. To invert a move we can apply it three times.

```py
import random

import pocket_cube

lookup = pocket_cube.build_lookup_table()

cube = random.choice(list(lookup.keys()))

while move := lookup[cube]:
    inverse = move.translate(move).translate(move)
    print('move', pocket_cube.moves.index(inverse))
    cube = cube.translate(inverse)
```
