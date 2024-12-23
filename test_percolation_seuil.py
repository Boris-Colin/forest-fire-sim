from random import sample, randrange


def random_forest(p, n):
    units = [(line, col) for col in range(n) for line in range(n)]
    ntrees = int(n**2*p)
    trees = sample(units, ntrees)
    states = [[0]*n for _ in range(n)]
    for (i, j) in trees:
        states[i][j] = 1
    return states, trees


def voisins(n, i, j):
    return [(a, b) for (a, b) in
            [(i, j+1), (i, j-1), (i-1, j), (i+1, j)]
            if a in range(n) and b in range(n)]


def start_fire(states, trees):
    i, j = trees[randrange(len(trees))]
    states[i][j] = 2
    return (i, j)


def update_states(states, fires):
    n = len(states)
    to_fire = []
    for (line, col) in fires:
        for (i, j) in voisins(n, line, col):
            if states[i][j] == 1:
                to_fire.append((i, j))
    for (line, col) in to_fire:
        states[line][col] = 2
    for (line, col) in fires:
        states[line][col] = 3

    return list(set(to_fire))


def test(n, p, repet):
    stats = []
    for _ in range(repet):
        states, trees = random_forest(p, n)
        i, j = start_fire(states, trees)
        ntrees = len(trees)
        nfire = 1
        foyers = [(i, j)]
        while True:
            foyers = update_states(states, foyers)
            fire = len(foyers)
            nfire += fire
            if fire == 0:
                break
        stats.append(nfire/ntrees)
    return sum(stats)/repet


n = 150
repet = 100
f = lambda p:test(n, p, repet)
P = [0.5+k/1000 for k in range(0, 201, 5)]
Q = list(map(f, P))
