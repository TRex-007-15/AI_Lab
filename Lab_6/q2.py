from collections import deque

# Constants
ACTIONS = {'L': (0, -1), 'R': (0, 1), 'U': (-1, 0), 'D': (1, 0)}

# Function to check if a cell is within the maze boundaries
def is_valid(x, y, maze):
    return 0 <= x < len(maze) and 0 <= y < len(maze[0])

# Function to calculate the utility score for the current state
def calculate_utility(maze, player, depth):
    if depth == 0:
        return 0

    # Define the opponent player
    opponent = 'B' if player == 'A' else 'A'

    # Check if the game is over
    if not any(3 in row for row in maze):
        return 0  # Game over, return a neutral score

    # Initialize utility
    utility = float('-inf') if player == 'A' else float('inf')

    # Find the player's current position
    player_position = None

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == player:
                player_position = (i, j)

    if player_position is None:
        return 0  # Player's position not found, return a neutral score

    # Iterate through possible actions
    for action, (dx, dy) in ACTIONS.items():
        new_maze = [row[:] for row in maze]  # Copy the maze to avoid modifying the original

        # Calculate the new position after taking the action
        new_x, new_y = player_position[0] + dx, player_position[1] + dy

        # Check if the new position is valid
        if is_valid(new_x, new_y, new_maze) and new_maze[new_x][new_y] != 1:
            # Move the player to the new position
            new_maze[player_position[0]][player_position[1]] = 0
            new_maze[new_x][new_y] = player

            # Recursively calculate utility for the opponent's turn
            opponent_utility = calculate_utility(new_maze, opponent, depth - 1)

            # Update the utility based on Minimax rules
            if player == 'A':
                utility = max(utility, opponent_utility)
            else:
                utility = min(utility, opponent_utility)

    return utility

# Function to find the best action for the current player using Minimax
def find_best_action(maze, player):
    best_action = None
    best_utility = float('-inf') if player == 'A' else float('inf')

    # Find the player's current position
    player_position = None

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == player:
                player_position = (i, j)

    if player_position is None:
        return None  # Player's position not found, return None

    # Iterate through possible actions
    for action, (dx, dy) in ACTIONS.items():
        new_maze = [row[:] for row in maze]  # Copy the maze to avoid modifying the original

        # Calculate the new position after taking the action
        new_x, new_y = player_position[0] + dx, player_position[1] + dy

        # Check if the new position is valid
        if is_valid(new_x, new_y, new_maze) and new_maze[new_x][new_y] != 1:
            # Move the player to the new position
            new_maze[player_position[0]][player_position[1]] = 0
            new_maze[new_x][new_y] = player

            # Calculate the utility using Minimax
            utility = calculate_utility(new_maze, player, depth=2)  # Adjust depth as needed

            # Update the best action and utility
            if (player == 'A' and utility > best_utility) or (player == 'B' and utility < best_utility):
                best_action = action
                best_utility = utility

    return best_action

# Function to play a round of the game using Minimax
def play_round_with_minimax(maze):
    # Initialize the player
    current_player = 'A'

    # Initialize visiting sequences
    visiting_sequence_A = []
    visiting_sequence_B = []

    while True:
        # Check if the game is over
        if not any(3 in row for row in maze):
            return maze, visiting_sequence_A, visiting_sequence_B

        # Find the best action for the current player using Minimax
        best_action = find_best_action(maze, current_player)

        # If there are no valid moves left, terminate the game
        if best_action is None:
            return maze, visiting_sequence_A, visiting_sequence_B

        # Perform the best action
        # Find the player's current position
        player_position = None

        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == current_player:
                    player_position = (i, j)

        # Calculate the new position after taking the best action
        new_x, new_y = player_position[0] + ACTIONS[best_action][0], player_position[1] + ACTIONS[best_action][1]

        # Move the player to the new position
        maze[player_position[0]][player_position[1]] = 0
        maze[new_x][new_y] = current_player

        # Update visiting sequence for the current player
        if current_player == 'A':
            visiting_sequence_A.append((new_x, new_y))
        else:
            visiting_sequence_B.append((new_x, new_y))

        # Switch to the next player
        current_player = 'B' if current_player == 'A' else 'A'

# Main function to play one round of the game with Minimax
def play_game_with_minimax():
    maze = [
        ['A', 0, 0, 0, 1],
        [0, 1, 0, 0, 3],
        [0, 3, 0, 1, 1],  # Starting position for Agent A (2)
        [0, 1, 0, 0, 1],
        [3, 0, 0, 4, 3]   # Reward locations (3)
    ]

    print("Initial Maze:")
    for row in maze:
        print(row)
    print()

    result, visiting_sequence_A, visiting_sequence_B = play_round_with_minimax(maze)

    # Find the winner based on the result
    if result.count('A') > result.count('B'):
        winner = 'A'
    elif result.count('B') > result.count('A'):
        winner = 'B'
    else:
        winner = 'Tie'

    # Print the visiting sequence for each agent and the winner
    print("Visiting Sequence for Agent A:")
    for row in result:
        print(row)
    print(f"Winner: Agent {winner}")

    # Save the visiting sequences to a file
    with open("out_minimax.txt", "w") as output_file:
        output_file.write("Visiting Sequence for Agent A:\n")
        for x, y in visiting_sequence_A:
            output_file.write(f"{x}, {y}\n")

        output_file.write("\nVisiting Sequence for Agent B:\n")
        for x, y in visiting_sequence_B:
            output_file.write(f"{x}, {y}\n")

        output_file.write(f"\nWinner: Agent {winner}")

# Play one round of the game using Minimax
play_game_with_minimax()

