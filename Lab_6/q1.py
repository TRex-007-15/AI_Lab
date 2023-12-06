from collections import deque

# Define possible actions
ACTIONS = {'L': (0, -1), 'R': (0, 1), 'U': (-1, 0), 'D': (1, 0)}

# Function to check if a cell is within the maze boundaries
def is_valid(x, y, maze):
    return 0 <= x < len(maze) and 0 <= y < len(maze[0])

# Function to find the shortest path from start to target using BFS
def shortest_path(maze, start, target):
    visited = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]
    queue = deque([(start[0], start[1], 0)])  # (x, y, steps)
    visited[start[0]][start[1]] = True

    while queue:
        x, y, steps = queue.popleft()

        if (x, y) == target:
            return steps

        for action, (dx, dy) in ACTIONS.items():
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y, maze) and not visited[new_x][new_y] and maze[new_x][new_y] != 1:
                visited[new_x][new_y] = True
                queue.append((new_x, new_y, steps + 1))

    return float('inf')

# Function to play a round of the game
def play_round(maze, round_num):
    start_positions = []
    reward_positions = []
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 2:
                start_positions.append((i, j))
            elif maze[i][j] == 3:
                reward_positions.append((i, j))

    steps_A = shortest_path(maze, start_positions[0], reward_positions[0])
    steps_B = shortest_path(maze, start_positions[0], reward_positions[1])  # Both agents go for different rewards

    if steps_A < steps_B:
        winner = 'A'
    elif steps_B < steps_A:
        winner = 'B'
    else:
        winner = 'Tie'

    print(f"\nRound {round_num + 1} - Agent A's steps: {steps_A}")
    print(f"Round {round_num + 1} - Agent B's steps: {steps_B}")
    print(f"Round {round_num + 1} Winner: Agent {winner}")

    return winner

# Function to play the game for 10 rounds
def play_game():
    rounds = 10
    wins_A, wins_B = 0, 0

    with open("out_advsearch.txt", "w") as output_file:
        for round_num in range(rounds):
            maze = [
                [2, 0, 0, 0, 1],
                [0, 1, 0, 0, 3],
                [0, 3, 0, 1, 1],  # Starting position for Agent A (2)
                [0, 1, 0, 0, 1],
                [3, 0, 0, 4, 3]   # Reward locations (3)
            ]

            winner = play_round(maze, round_num)

            if winner == 'A':
                wins_A += 1
            elif winner == 'B':
                wins_B += 1

            output_file.write(f"Round {round_num + 1} Winner: Agent {winner}\n")

    print("\nGame Over")
    print(f"Agent A wins: {wins_A} rounds")
    print(f"Agent B wins: {wins_B} rounds")
    if wins_A > wins_B:
        print("Overall Winner: Agent A")
        with open("out_advsearch.txt", "a") as output_file:
            output_file.write("Overall Winner: Agent A\n")
    elif wins_B > wins_A:
        print("Overall Winner: Agent B")
        with open("out_advsearch.txt", "a") as output_file:
            output_file.write("Overall Winner: Agent B\n")
    else:
        print("Overall Winner: Tie")
        with open("out_advsearch.txt", "a") as output_file:
            output_file.write("Overall Winner: Tie\n")

# Play the game
play_game()
