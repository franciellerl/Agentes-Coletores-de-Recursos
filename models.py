import random

#criação do grid
def create_grid(rows, cols):
    return [['Vazio' for _ in range(cols)] for _ in range(rows)]

#criação dos rios
def add_river(grid):
    rows, cols = len(grid), len(grid[0])
    river_row = random.randint(0, rows - 1)
    for col in range(cols):
        grid[river_row][col] = 'Rio'
    return grid

#criação das montanhas
def add_mountains(grid, mountain_count):
    rows, cols = len(grid), len(grid[0])
    for _ in range(mountain_count):
        while True:
            row, col = random.randint(0, rows - 1), random.randint(0, cols - 1)
            if grid[row][col] == 'Vazio':
                grid[row][col] = 'Montanha'
                break
    return grid

#distribuição dos recursos
def distribute_resources(grid, rarity):
    rows, cols = len(grid), len(grid[0])
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 'Vazio':
                obj = random.choices(
                    population=list(rarity.keys()) + ['Vazio'],
                    weights=list(rarity.values()) + [10],
                    k=1
                )[0]
                grid[row][col] = obj
    return grid

#movimentação dos agentes
def move_agent(grid, agent_pos, direction):
    rows, cols = len(grid), len(grid[0])
    x, y = agent_pos
    dx, dy = direction
    nx, ny = x + dx, y + dy

    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 'Montanha' and grid[nx][ny] != 'Rio':
        return nx, ny
    return x, y

#coleta de recursos
def collect_resource(grid, agent_pos, allowed_resources):
    x, y = agent_pos
    if grid[x][y] in allowed_resources:
        collected = grid[x][y]
        grid[x][y] = 'Vazio'
        return collected
    return None

def random_position(grid):
    rows, cols = len(grid), len(grid[0])
    while True:
        x, y = random.randint(0, rows - 1), random.randint(0, cols - 1)
        if grid[x][y] == 'Vazio':
            return x, y
