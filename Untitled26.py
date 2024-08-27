#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pygame
import sys

pygame.init()

BOARD_SIZE = 5
SQUARE_SIZE = 100
WIDTH, HEIGHT = BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE
WHITE = (255, 255, 255)
GREEN = (144, 238, 144)
BLUE = (173, 216, 230)
YELLOW = (255, 255, 0)
FONT = pygame.font.SysFont(None, 35)


colors = [(255, 255, 255), (0, 0, 0)]


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("5x5 Chess-Like Game")

def draw_board(grid):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            text = grid[row][col]
            if text:
                label = FONT.render(text, True, (0, 0, 0))
                screen.blit(label, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4))

def main():
    grid = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    current_player = "A"
    selected_char = None
    
  
    for i in range(BOARD_SIZE):
        grid[0][i] = f"B-{i+1}"
        grid[BOARD_SIZE-1][i] = f"A-{i+1}"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x //= SQUARE_SIZE
                y //= SQUARE_SIZE

                if selected_char:
           
                    if is_valid_move(selected_char, (x, y), grid, current_player):
                        char_x, char_y = selected_char
                        grid[x][y] = grid[char_x][char_y]
                        grid[char_x][char_y] = ""
                        selected_char = None
                        current_player = "B" if current_player == "A" else "A"
                    else:
                        print("Invalid move!")
                else:
               
                    if grid[y][x].startswith(current_player):
                        selected_char = (x, y)

        draw_board(grid)
        pygame.display.flip()

def is_valid_move(start, end, grid, player):
    start_x, start_y = start
    end_x, end_y = end
    character = grid[start_y][start_x]
    

    if end_x < 0 or end_y < 0 or end_x >= BOARD_SIZE or end_y >= BOARD_SIZE:
        return False
    
er
    if grid[end_y][end_x].startswith(player):
        return False
   
    dx, dy = end_x - start_x, end_y - start_y
    if "P1" in character:
        return abs(dx) <= 1 and abs(dy) <= 1
    elif "H1" in character:
        return (dx == 0 or dy == 0) and (abs(dx) <= 2 and abs(dy) <= 2)
    elif "H2" in character:
        return abs(dx) == 2 and abs(dy) == 2

    return False

if __name__ == "__main__":
    main()


# In[9]:


import pygame
import sys

pygame.init()


WIDTH, HEIGHT = 600, 600
GRID_SIZE = 5
CELL_SIZE = WIDTH // GRID_SIZE


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

FONT = pygame.font.SysFont(None, 24)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess-like Game')

grid = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
turn = 'A'
characters = {
    'A': {'P1': (0, 0), 'P2': (0, 1), 'H1': (0, 2), 'H2': (0, 3), 'P3': (0, 4)},
    'B': {'P4': (4, 0), 'P5': (4, 1), 'H3': (4, 2), 'H4': (4, 3), 'P6': (4, 4)}
}

def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(screen, color, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_characters():
    for player in characters:
        for name, (row, col) in characters[player].items():
            color = RED if player == 'A' else BLUE
            pygame.draw.circle(screen, color, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
            text = FONT.render(name, True, BLACK)
            screen.blit(text, (col * CELL_SIZE + 5, row * CELL_SIZE + 5))

def move_character(player, char_name, move):
    if char_name not in characters[player]:
        return False
    
    row, col = characters[player][char_name]
    if move == 'L':
        col -= 1
    elif move == 'R':
        col += 1
    elif move == 'F':
        row -= 1
    elif move == 'B':
        row += 1
    elif move == 'FL':
        row -= 1
        col -= 1
    elif move == 'FR':
        row -= 1
        col += 1
    elif move == 'BL':
        row += 1
        col -= 1
    elif move == 'BR':
        row += 1
        col += 1

    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        if grid[row][col] == '' or grid[row][col][0] != player:
            characters[player][char_name] = (row, col)
            if grid[row][col] != '':
                opponent = 'B' if player == 'A' else 'A'
                for key in list(characters[opponent].keys()):
                    if characters[opponent][key] == (row, col):
                        del characters[opponent][key]
                        break
            return True
    return False

def game_loop():
    global turn
    selected_char = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  
                    selected_char = 'P1'  
                elif event.key == pygame.K_s and selected_char:  
                    move_character(turn, selected_char, 'R')  
                    turn = 'B' if turn == 'A' else 'A'
                elif event.key == pygame.K_w and selected_char:
                    move_character(turn, selected_char, 'F')  
                    turn = 'B' if turn == 'A' else 'A'
                elif event.key == pygame.K_d and selected_char:
                    move_character(turn, selected_char, 'L')  
                    turn = 'B' if turn == 'A' else 'A'
                elif event.key == pygame.K_x and selected_char:
                    move_character(turn, selected_char, 'B')  
                    turn = 'B' if turn == 'A' else 'A'

        screen.fill(BLACK)
        draw_grid()
        draw_characters()
        pygame.display.flip()

if __name__ == '__main__':
    game_loop()


# In[ ]:




