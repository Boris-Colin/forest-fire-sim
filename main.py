from random import sample, choices
from tkinter import Tk, Canvas, Scale, Button, Label, N, ALL
import heapq

TYPE_DARK = 5  # plutôt utiliser ça que des 'nombres magiques'
TYPE_LIGHT = 4
D = []  # liste utilisée pour calculer les chemins


def dijkstra(states, start, end):
    n = len(states)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Only 4 cardinal directions

    # Initialize distances and visited set
    distances = [[float('inf')] * n for _ in range(n)]
    visited = [[False] * n for _ in range(n)]
    distances[start[0]][start[1]] = 0

    # Priority queue to hold cells to explore
    pq = [(0, start)]  # (distance, (x, y))

    while pq:
        current_distance, (x, y) = heapq.heappop(pq)

        if visited[x][y]:
            continue
        visited[x][y] = True

        # Stop if we reached the end point
        if (x, y) == end:
            break

        # Check neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < n and 0 <= ny < n:  # Ensure within bounds
                if states[nx][ny] in {1, 4, 7} and not visited[nx][ny]:  # Only go through trees
                    new_distance = current_distance + 1
                    if new_distance < distances[nx][ny]:
                        distances[nx][ny] = new_distance
                        heapq.heappush(pq, (new_distance, (nx, ny)))

    return distances[end[0]][end[1]] if distances[end[0]][end[1]] != float('inf') else "Unreachable"


def print_distances(distances):
    for row in distances:
        print(" ".join(f"{cell if cell != float('inf') else 'inf':>4}" for cell in row))


COLORS = ["ivory", "lime green", "red", "gray75", "dark green", "orange", "black", "pink"]


def random_forest(p, n):
    units = [(line, col) for col in range(n) for line in range(n)]
    ntrees = int(n**2 * p)  # nombre d'arbres au total
    states = [[0] * n for _ in range(n)]  # initialise une matrice de 0
    tree_choices = [1, 4]  # 1 for regular trees, 4 for dark green trees
    probabilities = [0.95, 0.05]  # 70% regular, 30% dark green
    trees = sample(units, ntrees)  # fonction du module random crée une distribution aléatoire
    """
    J'aurais aussi pu repasser sur la grille des states et lancé une 'pièce' à chaque fois pour savoir si je
    mettais un arbre, mais c'est bien comme ça aussi"""
    for (i, j) in trees:
        states[i][j] = choices(tree_choices, probabilities)[0]
    return states


def voisins(n, i, j, dark_green=False):
    neighbors = [(i, j + 1), (i, j - 1), (i - 1, j), (i + 1, j)]
    if dark_green:  # Les diagonales en plus pour les arbres sombres
        print('dark green')
        neighbors += [(i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), (i + 1, j + 1)]
    return [(a, b) for (a, b) in neighbors if a in range(n) and b in range(n)]


def fill_cell(states, line, col):
    A = (unit * col, unit * line)
    B = (unit * (col + 1), unit * (line + 1))
    state = states[line][col]
    color = COLORS[state]
    cnv.create_rectangle(A, B, fill=color, outline='')


def fill(states):
    # fonction qui colorie l'interface graphique correctement
    n = len(states)
    for line in range(n):
        for col in range(n):
            fill_cell(states, line, col)


def update_states(states):
    global turns, running
    n = len(states)
    #print('States: ', states)
    to_fire = []
    for line in range(n):
        for col in range(n):
            # on regarde l'état original
            original_state = states[line][col]
            print(original_state)

            if original_state == 2:  # feu normal
                states[line][col] = 3  # brulé
                dark_green = (original_state == 4)
                # print("Detected", dark_green)  # Check if dark green tree
                cell_voisins = voisins(n, line, col, dark_green)

                for (i, j) in cell_voisins:
                    if states[i][j] in {1, 4}:  # Trees only
                        to_fire.append((i, j))

            elif original_state == 5:  # Control fire
                if turns >= 2:
                    states[line][col] = 3  # Burned-out after 2 turns
                else:
                    dark_green = (original_state == 4)  # Check if it was a dark green tree
                    cell_voisins = voisins(n, line, col, dark_green)

                    for (i, j) in cell_voisins:
                        if states[i][j] in {1, 4}:  # Trees only
                            to_fire.append((i, j))

    for (line, col) in to_fire:
        if states[line][col] != 6:  # Skip black cells
            states[line][col] = 5 if controlled_fire_mode else 2


def init():
    D.clear()
    global states, cpt, ntrees, running, turns, controlled_fire_mode

    p = int(curseur.get()) / 100
    running = False
    cpt = 0
    turns = 0
    controlled_fire_mode = False
    lbl["text"] = "0 % | Turns: 0"  # indicateurs
    curseur["state"] = 'normal'
    states = random_forest(p, n)
    ntrees = sum(states[i][j] in {1, 4} for i in range(n) for j in range(n))  # compter l'ensemble des arbes
    cnv.delete(ALL)
    fill(states)


def set_density(states, p):
    # permet d'ajuster la densitée
    n = len(states)
    trees = [(i, j) for i in range(n) for j in range(n) if states[i][j] in {1, 4}]
    nontrees = [(i, j) for i in range(n) for j in range(n) if states[i][j] == 0]
    density = len(trees) / n**2
    new_trees = int(n * n * p)
    delta = abs(new_trees - len(trees))
    if new_trees >= len(trees):
        for (i, j) in sample(nontrees, delta):
            states[i][j] = choices([1, 4], [0.7, 0.3])[0]
    else:
        for (i, j) in sample(trees, delta):
            states[i][j] = 0


def make_forest(percent):
    D.clear()
    global ntrees

    cnv.delete("all")
    p = float(percent) / 100
    set_density(states, p)
    ntrees = sum(states[i][j] in {1, 4} for i in range(n) for j in range(n))  # Recalculate
    fill(states)


def propagate():
    # Explicite, calcule la propagation du feu
    global cpt, running, turns

    update_states(states)
    nfires = sum(states[i][j] in {2, 5} for i in range(n) for j in range(n))
    cpt += nfires
    turns += 1
    percent = int(cpt / ntrees * 100)
    cnv.delete("all")
    fill(states)
    lbl["text"] = f"{percent} % | Turns: {turns}"
    if nfires == 0 or (controlled_fire_mode and turns >= 2):
        running = False
        return
    cnv.after(150, propagate)


def fire(event):
    global running, cpt, turns

    i, j = event.y // unit, event.x // unit
    if states[i][j] in {1, 4}:  # Can start fire on either type of tree
        states[i][j] = 5 if controlled_fire_mode else 2  # Controlled or regular fire
        fill_cell(states, i, j)

        cpt += 1
        if not running:
            running = True
            turns = 0  # Reset turns for controlled fire
            curseur["state"] = 'disabled'
            propagate()


def make_black(event):
    i, j = event.y // unit, event.x // unit
    states[i][j] = 6  # Turn the cell black
    fill_cell(states, i, j)


def pre_dijkstra(event):
    i, j = event.y // unit, event.x // unit
    D.append((i, j))
    states[i][j] = 7  # Turn the cell purple
    fill_cell(states, i, j)


def toggle_mode():
    global controlled_fire_mode
    controlled_fire_mode = not controlled_fire_mode
    mode_btn["text"] = "Controlled Fire" if controlled_fire_mode else "Normal Fire"


n = 50
unit = 10


def compute_dijkstra():
    global states
    d_n = len(D)
    start = D[d_n - 2]  # bien pour l'instant, mais trop dépendant du hasard si (0, 0)
    end = D[d_n-1]
    # je give up pour l'instant, on va juste faire ça entre les deux derniers

    distance = dijkstra(states, start, end)

    # Print distance to the end point
    print(f"Distance from {start} to {end}: {distance}")


# Affichage
root = Tk()
cnv = Canvas(root, width=unit * n - 2, height=unit * n - 2, background="ivory")
cnv.grid(row=0, column=0, rowspan=5)

btn = Button(root, text="Nouveau", font='Arial 15 bold', command=init, width=8)
btn.grid(row=0, column=1, sticky=N)

btn_dijkstra = Button(root, text="Run Dijkstra", command=compute_dijkstra, font='Arial 10', width=12)
btn_dijkstra.grid(row=1, column=1, sticky='n')

lbl = Label(root, text="0 % | Turns: 0", font='Arial 15 bold', bg='pink', width=15)
lbl.grid(row=3, column=1, sticky=N)

mode_btn = Button(root, text="Normal Fire", font='Arial 10', command=toggle_mode, width=12)
mode_btn.grid(row=2, column=1, sticky=N)

# Bind left-click for fire and right-click for black cells
# middle button for dijkstra
cnv.bind("<Button-1>", fire)
cnv.bind("<Button-2>", pre_dijkstra)
cnv.bind("<Button-3>", make_black)

curseur = Scale(root, orient="vertical", command=make_forest, from_=100,
                to=0, length=200)
curseur.set(60)
curseur.grid(row=4, column=1)

init()

root.mainloop()
