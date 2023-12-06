from collections import deque
import heapq
import math
class MazeSolver:
    def __init__(self, rows, cols, start, goal, obstacles):
        self.rows = rows
        self.cols = cols
        self.start = start
        self.goal = goal
        self.obstacles = obstacles
        self.explored = set()  # To keep track of explored blocks
        self.search_cost = 0   # To keep track of the total search cost

    def is_valid_move(self, x, y):
        return 1 <= x <= self.rows and 1 <= y <= self.cols and (x, y) not in self.obstacles
    
    def heuristic(self, x, y):
        # Define a heuristic function (e.g., Manhattan distance)
        return abs(x - self.goal[0]) + abs(y - self.goal[1])

    def solve_maze_dfs(self):
        stack = [(self.start[0], self.start[1])]
        while stack:
            x, y = stack.pop()
            self.search_cost += 1
            if (x, y) == self.goal:
                return True
            if (x, y) not in self.explored:
                self.explored.add((x, y))
                # Push valid neighbors onto the stack
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if self.is_valid_move(nx, ny):
                        stack.append((nx, ny))
        return False

    def solve_maze_bfs(self):
        queue = deque([(self.start[0], self.start[1])])
        while queue:
            x, y = queue.popleft()
            self.search_cost += 1
            if (x, y) == self.goal:
                return True
            if (x, y) not in self.explored:
                self.explored.add((x, y))
                # Enqueue valid neighbors
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if self.is_valid_move(nx, ny):
                        queue.append((nx, ny))
        return False

    def solve_maze_dls(self, limit):
        stack = [(self.start[0], self.start[1], 0)]
        while stack:
            x, y, depth = stack.pop()
            self.search_cost += 1
            if depth > limit:
                continue  # Depth limit reached, backtrack
            if (x, y) == self.goal:
                return True
            if (x, y) not in self.explored:
                self.explored.add((x, y))
                # Push valid neighbors onto the stack
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if self.is_valid_move(nx, ny):
                        stack.append((nx, ny, depth + 1))
        return False
    def solve_maze_ucs(self):
        # Uniform Cost Search implementation
        pq = [(0, self.start[0], self.start[1])]
        cost_so_far = {(self.start[0], self.start[1]): 0}

        while pq:
            current_cost, x, y = heapq.heappop(pq)
            self.search_cost += 1

            if (x, y) == self.goal:
                return True

            if (x, y) not in self.explored:
                self.explored.add((x, y))

                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy

                    if self.is_valid_move(nx, ny):
                        new_cost = current_cost + 1  # Uniform cost

                        if (nx, ny) not in cost_so_far or new_cost < cost_so_far[(nx, ny)]:
                            cost_so_far[(nx, ny)] = new_cost
                            heapq.heappush(pq, (new_cost, nx, ny))

        return False

    def solve_maze_gbfs(self):
        # Greedy Best First Search implementation
        pq = [(self.heuristic(self.start[0], self.start[1]), self.start[0], self.start[1])]

        while pq:
            _, x, y = heapq.heappop(pq)
            self.search_cost += 1

            if (x, y) == self.goal:
                return True

            if (x, y) not in self.explored:
                self.explored.add((x, y))

                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy

                    if self.is_valid_move(nx, ny):
                        heapq.heappush(pq, (self.heuristic(nx, ny), nx, ny))

        return False

    def solve_maze_astar(self):
        # A* Algorithm implementation
        pq = [(0, self.start[0], self.start[1])]
        cost_so_far = {(self.start[0], self.start[1]): 0}

        while pq:
            current_cost, x, y = heapq.heappop(pq)
            self.search_cost += 1

            if (x, y) == self.goal:
                return True

            if (x, y) not in self.explored:
                self.explored.add((x, y))

                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy

                    if self.is_valid_move(nx, ny):
                        new_cost = cost_so_far[(x, y)] + 1  # Cost to reach the neighbor
                        if (nx, ny) not in cost_so_far or new_cost < cost_so_far[(nx, ny)]:
                            cost_so_far[(nx, ny)] = new_cost
                            priority = new_cost + self.heuristic(nx, ny)  # A* priority
                            heapq.heappush(pq, (priority, nx, ny))

        return False

    def find_solution(self, search_strategy, depth_limit=None):
        if search_strategy == 'dfs':
            return self.solve_maze_dfs()
        elif search_strategy == 'bfs':
            return self.solve_maze_bfs()
        elif search_strategy == 'dls':
            if depth_limit is not None:
                return self.solve_maze_dls(depth_limit)
        elif search_strategy == 'ucs':
            return self.solve_maze_ucs()
        elif search_strategy == 'gbfs':
            return self.solve_maze_gbfs()
        elif search_strategy == 'astar':
            return self.solve_maze_astar()
        else:
            return None

if __name__ == '__main__':
    # Increase the recursion limit to a higher value (optional)
    # sys.setrecursionlimit(10000)

    # Read input from the file
    with open('input.txt', 'r') as file:
        rows, cols = map(int, file.readline().split())
        start_x, start_y, goal_x, goal_y = map(int, file.readline().strip().split())
        obstacle_lines = file.readline().strip().split()
        obstacles = {(int(obstacle_lines[i]), int(obstacle_lines[i+1])) for i in range(0, len(obstacle_lines), 2)}
        search_strategy = file.readline().strip()
        depth_limit = 10 # You mentioned depth_limit as 3 in your example

    solver = MazeSolver(rows, cols, (start_x, start_y), (goal_x, goal_y), obstacles)

    result = solver.find_solution(search_strategy, depth_limit)

    # Write the result to an output file
    with open('output.txt', 'w') as file:
        if result:
            file.write("Sequence of blocks explored:\n")
            for block in sorted(solver.explored):
                file.write(f"{block[0]} {block[1]}\n")
            file.write(f"Total search cost: {solver.search_cost}\n")
        else:
            file.write("No path found.\n")
