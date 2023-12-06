import heapq

# Constants for directions
LEFT, RIGHT, UP, DOWN = (-1, 0), (1, 0), (0, -1), (0, 1)

# Define a class for the problem state
class State:
    def __init__(self, x, y, rewards, steps):
        self.x = x
        self.y = y
        self.rewards = rewards
        self.steps = steps

    # Implement a comparison method for priority queue
    def __lt__(self, other):
        # Compare states based on steps + heuristic
        return (self.steps + self.heuristic()) < (other.steps + other.heuristic())

    # Implement a heuristic function (Manhattan distance to the nearest reward)
    def heuristic(self):
        if not self.rewards:
            return 0
        min_dist = min(abs(self.x - rx) + abs(self.y - ry) for rx, ry in self.rewards)
        return min_dist

# Implement the A* algorithm
def astar(maze):
    rows, cols = len(maze), len(maze[0])
    start_x, start_y = None, None
    rewards = set()

    # Find the start position and collect rewards
    for x in range(rows):
        for y in range(cols):
            if maze[x][y] == 2:
                start_x, start_y = x, y
            elif maze[x][y] == 3:
                rewards.add((x, y))

    start_state = State(start_x, start_y, rewards, 0)
    priority_queue = [start_state]
    visited_sequence = []  # Store visited tiles

    while priority_queue:
        current_state = heapq.heappop(priority_queue)
        x, y = current_state.x, current_state.y

        if not current_state.rewards:
            # All rewards collected, exit
            return current_state.steps, visited_sequence

        visited_sequence.append((x, y))  # Record visited tile

        # Explore possible moves (left, right, up, down)
        for dx, dy in [(LEFT), (RIGHT), (UP), (DOWN)]:
            new_x, new_y = x + dx, y + dy

            if 0 <= new_x < rows and 0 <= new_y < cols and maze[new_x][new_y] != 1:
                new_rewards = current_state.rewards.copy()
                if (new_x, new_y) in new_rewards:
                    new_rewards.remove((new_x, new_y))

                new_state = State(new_x, new_y, new_rewards, current_state.steps + 1)
                heapq.heappush(priority_queue, new_state)

    # No path to collect all rewards
    return -1, visited_sequence

# Read input from a text file
def read_maze_from_file(filename):
    with open(filename, 'r') as file:
        maze = [[int(tile) for tile in line.strip().split()] for line in file.readlines()]
    return maze

# Write visited sequence to an output file
def write_visited_sequence_to_file(sequence, filename):
    with open(filename, 'w') as file:
        for x, y in sequence:
            file.write(f"{x} {y}\n")

# Define the input and output filenames
input_filename = 'input.txt'
output_filename = 'out_astar.txt'

# Read the maze from the input file
maze = read_maze_from_file(input_filename)

# Run the A* algorithm
result, visited_sequence = astar(maze)

# Write the visited sequence to the output file
write_visited_sequence_to_file(visited_sequence, output_filename)

if result == -1:
    print("No path to collect all rewards.")
else:
    print(f"Minimum steps to collect all rewards: {result}")
