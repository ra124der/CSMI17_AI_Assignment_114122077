import random
import heapq
import time
import numpy as np
import matplotlib.pyplot as plt

# 3 heuristic functions
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5

def diagonal(a, b):
    return max(abs(a[0]-b[0]), abs(a[1]-b[1]))

# A* function
def astar(grid, start, goal, heuristic):
    rows, cols = grid.shape
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(start, goal), 0, start))
    came_from = {}
    g_score = {start: 0}
    explored = 0

    while open_list:
        _, cost, current = heapq.heappop(open_list)
        explored += 1

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, explored

        # 4 direction movement
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
                new_g = g_score[current] + 1
                if (nx, ny) not in g_score or new_g < g_score[(nx, ny)]:
                    g_score[(nx, ny)] = new_g
                    f = new_g + heuristic((nx, ny), goal)
                    heapq.heappush(open_list, (f, new_g, (nx, ny)))
                    came_from[(nx, ny)] = current

    return None, explored

# generate random grid
def make_grid(n=10, obstacle_prob=0.25):
    grid = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            if random.random() < obstacle_prob:
                grid[i][j] = 1
    start = (random.randint(0, n-1), random.randint(0, n-1))
    goal = (random.randint(0, n-1), random.randint(0, n-1))
    while grid[start] == 1 or grid[goal] == 1 or start == goal:
        start = (random.randint(0, n-1), random.randint(0, n-1))
        goal = (random.randint(0, n-1), random.randint(0, n-1))
    return grid, start, goal

# print grid with path
def print_grid(grid, start, goal, path=None):
    path_set = set(path) if path else set()
    for i in range(grid.shape[0]):
        row = ""
        for j in range(grid.shape[1]):
            if (i,j) == start:
                row += "S "
            elif (i,j) == goal:
                row += "G "
            elif (i,j) in path_set:
                row += "* "
            elif grid[i,j] == 1:
                row += "# "
            else:
                row += ". "
        print(row)
    print()

# compare heuristics and display metrics
def compare(runs=5, size=10):
    heuristics = {
        "Manhattan": manhattan,
        "Euclidean": euclidean,
        "Diagonal": diagonal
    }

    results = {h: {"time": [], "nodes": [], "length": []} for h in heuristics}

    for i in range(runs):
        grid, start, goal = make_grid(size)
        print(f"--- Run {i+1} --- Start: {start}, Goal: {goal}\n")
        for name, h in heuristics.items():
            t0 = time.time()
            path, explored = astar(grid, start, goal, h)
            t1 = time.time()
            exec_time = t1 - t0
            path_len = len(path) if path else np.nan
            results[name]["time"].append(exec_time)
            results[name]["nodes"].append(explored)
            results[name]["length"].append(path_len)
            print(f"Heuristic: {name}")
            print(f"  Execution Time: {exec_time:.5f} s")
            print(f"  Nodes Explored: {explored}")
            print(f"  Path Length: {path_len}\n")

    # Print averages table
    print("\n=== Average Metrics for Each Heuristic ===")
    print(f"{'Heuristic':<12}{'Average Time (s)':<20}{'Average Nodes Explored':<25}{'Average Path Length':<20}")
    for name in heuristics:
        avg_time = np.nanmean(results[name]["time"])
        avg_nodes = np.nanmean(results[name]["nodes"])
        avg_length = np.nanmean(results[name]["length"])
        print(f"{name:<12}{avg_time:<20.5f}{int(avg_nodes):<25}{avg_length:<20.2f}")

    return results

# plot results
def plot(results):
    for metric in ["time", "nodes", "length"]:
        plt.figure()
        for h in results:
            plt.plot(results[h][metric], label=h, marker='o')
        plt.title(f"{metric.capitalize()} comparison")
        plt.xlabel("Run")
        plt.ylabel(metric.capitalize())
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Sample grid for screenshot
    grid, start, goal = make_grid(10, 0.25)
    path, explored = astar(grid, start, goal, manhattan)
    print("Sample Grid with Path (Manhattan heuristic):")
    print_grid(grid, start, goal, path)

    # Run and display metrics
    data = compare(runs=5, size=10)
    plot(data)
