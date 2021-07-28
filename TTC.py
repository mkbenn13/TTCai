import pygame
import math
import random
import time
import json
import pickle
import sys
# Initializing Pygame
pygame.init()

# Screen
WIDTH = 500
ROWS = 3
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("TicTacToe")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
first_turn = True
needed_moves = False
nums = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)] #[(2,0), (2,2), (0,1), (0,0), (1,1), (2,1), (0,2), (1,0), (1,2)] 
coords = []
random.shuffle(nums)

game_data = {}
current_game = {}
move_num = 1
game_num = 0

first_call = True
second_call = True
f = open('storage\\store.pckl', 'rb')
while first_call:
    try:
        game_num = pickle.load(f)
        first_call = False
    except EOFError:
        game_num = 1
        first_call = False

while second_call:
    try:
        game_data_loader = json.load(open('storage\\game_data.json'))
        l = list(game_data_loader.items())
        random.shuffle(l)
        game_data = dict(l)
        second_call = False
    except json.decoder.JSONDecodeError:
        game_data = {}
        second_call = False
game_data|={'game_'+str(game_num):{}}


# Images
X_IMAGE = pygame.transform.scale(pygame.image.load("images\\X.png"), (150, 150))
O_IMAGE = pygame.transform.scale(pygame.image.load("images\\O.png"), (150, 150))

# Fonts
END_FONT = pygame.font.SysFont('courier', 40)

def draw_grid():
    gap = WIDTH // ROWS #166.67

    # Starting points
    x = 0 #0, 0 
    y = 0

    for i in range(ROWS):
        x = i * gap

        pygame.draw.line(win, GRAY, (x, 0), (x, WIDTH), 3)
        pygame.draw.line(win, GRAY, (0, x), (WIDTH, x), 3)

# Place x or o as a player
def click(game_array):
    global x_turn, o_turn, images, current_char

    # Mouse position
    m_x, m_y = pygame.mouse.get_pos()

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x, y, char, can_play = game_array[i][j]

            # Distance between mouse and the centre of the square
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)

            # If it's inside the square
            if dis < WIDTH // ROWS // 2 and can_play:
                if x_turn:  # If it's X's turn
                    images.append((x, y, X_IMAGE))
                    x_turn = False
                    o_turn = True
                    game_array[i][j] = (x, y, 'x', False)
                    current_char = 'o'
                    game_data["game_"+str(game_num)].update({
                    "move_"+str(move_num): {
                        "char":"x",
                        "coords":(x, y)
                        },
                    })
                    current_game.update({
                    "move_"+str(move_num): {
                        "char":"x",
                        "coords":(x, y)
                        },
                    })
                elif o_turn:  # If it's O's turn
                    images.append((x, y, O_IMAGE))
                    x_turn = True
                    o_turn = False
                    game_array[i][j] = (x, y, 'o', False)
                    current_char = 'x'
                    game_data["game_"+str(game_num)].update({
                "move_"+str(move_num): {
                    "char":"o",
                    "coords":(x, y)
                },
            })
                    current_game.update({
                "move_"+str(move_num): {
                    "char":"o",
                    "coords":(x, y)
                },
            })

# Use the check_board function to place x's or o's
def ai_counter(game_array, m):
    global x_turn, o_turn, images, move_num, game_data, current_char, game_num
    # if x_turn:
    #     return -1
    if m == -1:
        if x_turn:
            current_char = 'x'
        else:
            current_char = 'o'
        for game, value in game_data.items():
            if game == 'game_'+str(game_num):
                #print(game, 'game_'+str(game_num))
                break
            else:
                c=[move for move,value2 in game_data[game].items()]
                #for move, value2 in game_data[game].items()[0:-1]:
                for move in c[0: -1]:
                    #print(c)
                    for info, value3 in value[move].items():
                        if value3 == current_char == value['winner'] or make_game_array(game) == game_array:
                            #print(value['winner'])
                            m, x = game_data[game][move]['coords']
                            i, j = coord_convert(m, x)
                            #print(i, j, '2', move, value3)
                            x, y, char, can_play = game_array[i][j]
                            if can_play:
                                #print('2')
                                if x_turn and can_play:
                                    images.append((x, y, X_IMAGE))
                                    x_turn = False
                                    o_turn = True
                                    game_array[i][j] = (x, y, 'x', False)
                                    game_data["game_"+str(game_num)].update({
                                        "move_"+str(move_num): {
                                            "char":"x",
                                            "coords":(x, y)
                                        },
                                    })
                                    current_game.update({
                                        "move_"+str(move_num): {
                                            "char":"x",
                                            "coords":(x, y)
                                        },
                                    })
                                    return -1
                                elif o_turn and can_play:
                                    images.append((x, y, O_IMAGE))
                                    x_turn = True
                                    o_turn = False
                                    game_array[i][j] = (x, y, 'o', False)
                                    game_data["game_"+str(game_num)].update({
                                        "move_"+str(move_num): {
                                            "char":"o",
                                            "coords":(x, y)
                                        },
                                    })
                                    current_game.update({
                                        "move_"+str(move_num): {
                                            "char":"o",
                                            "coords":(x, y)
                                        },
                                    })
                                    return -1
                            else:
                                break        
    elif m!=-1:
        #print('1')
        i, j = m
        x, y, char, can_play = game_array[i][j]
        if x_turn and can_play:
            images.append((x, y, X_IMAGE))
            x_turn = False
            o_turn = True
            game_array[i][j] = (x, y, 'x', False)
            game_data["game_"+str(game_num)].update({
                "move_"+str(move_num): {
                    "char":"x",
                    "coords":(x, y)
                },
            })
            current_game.update({
                "move_"+str(move_num): {
                    "char":"x",
                    "coords":(x, y)
                },
            })
            return -1
        elif o_turn and can_play:
            images.append((x, y, O_IMAGE))
            x_turn = True
            o_turn = False
            game_array[i][j] = (x, y, 'o', False)
            game_data["game_"+str(game_num)].update({
                "move_"+str(move_num): {
                    "char":"o",
                    "coords":(x, y)
                },
            })
            current_game.update({
                "move_"+str(move_num): {
                    "char":"o",
                    "coords":(x, y)
                },
            })
            return -1
        i, j = nums[0]
        nums.pop(0)
        #print(i, j, '3')
        x, y, char, can_play = game_array[i][j]
        if x_turn and can_play:
            images.append((x, y, X_IMAGE))
            x_turn = False
            o_turn = True
            game_array[i][j] = (x, y, 'x', False)
            game_data["game_"+str(game_num)].update({
                "move_"+str(move_num): {
                    "char":"x",
                    "coords":(x, y)
                },
            })
            current_game.update({
                "move_"+str(move_num): {
                    "char":"x",
                    "coords":(x, y)
                },
            })
        elif o_turn and can_play:
            images.append((x, y, O_IMAGE))
            x_turn = True
            o_turn = False
            game_array[i][j] = (x, y, 'o', False)
            game_data["game_"+str(game_num)].update({
                "move_"+str(move_num): {
                    "char":"o",
                    "coords":(x, y)
                },
            })
            current_game.update({
                "move_"+str(move_num): {
                    "char":"o",
                    "coords":(x, y)
                },
            })
    return -1

# Create the game board and 2d array
def initialize_grid():
    dis_to_cen = 500 // 3 // 2 #83.4

    # Initializing the array
    game_array = [[None, None, None], [None, None, None], [None, None, None]]

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)

            # Adding centre coordinates
            game_array[i][j] = (x, y, "", True)

    return game_array

def coord_convert(i, j):
    for m in range(len(game_array)):
        for x in range(len(game_array[m])):
            if game_array[m][x][0] == i and game_array[m][x][1] == j:
                return(m, x)
    return (-1, -1)

def make_game_array(game):
    global move_num, game_data
    game_data_array = [[None, None, None], [None, None, None], [None, None, None]]

    c=[move for move, value2 in game_data[game].items()]
    for move in c[0: -1]:
        for info, value3 in game_data[game][move].items():
            if info == 'coords' and move == move_num:
                m, x = value3
                i, j = coord_convert(m, x)
                char = game_data[game][move]['char']
                game_data_array[i][j] = ((m, x, char, False))          

    for a in range(len(game_data_array)):
        for b in range(len(game_data_array[a])):
            if game_data_array[a][b] == None:
                dis_to_cen = 500 // 3 // 2
                x = dis_to_cen * (2 * b + 1)
                y = dis_to_cen * (2 * a + 1)
                game_data_array[a][b] = (x, y, "", True)

    return game_data_array
            

#def ai_learn():
    

# Check for win or loss that is one move away
def check_board(game_array):
    global board_check
    # Checking rows
    for row in range(len(game_array)):
        if game_array[row][0][2] == game_array[row][1][2] != '' and (game_array[row][2][2] == ''):
            #print(my_char + str(row)+"][2][2]1")
            return (row, 2)
        elif game_array[row][0][2] == game_array[row][2][2] != '' and (game_array[row][1][2] == ''):
            #print(my_char + str(row)+"][1][2]2")
            return (row, 1)
        elif game_array[row][1][2] == game_array[row][2][2] != '' and (game_array[row][0][2] == ''):
            #print(my_char + str(row)+"][0][2]3")
            return (row, 0)
    # Checking cols
    for col in range(len(game_array)):
        if game_array[0][col][2] == game_array[1][col][2] != '' and (game_array[2][col][2] == ''):
            #print(my_char + "[2]["+str(col)+"][2]4")
            return (2, col)
        elif game_array[0][col][2] == game_array[2][col][2] != '' and (game_array[1][col][2] == ''):
            #print(my_char + "[1]["+str(col)+"][2]5")
            return (1, col)
        elif game_array[1][col][2] == game_array[2][col][2] != '' and (game_array[0][col][2] == ''):
            #print(my_char + "[0]["+str(col)+"][2]6") 
            return (0, col)      
    # Checking Diagonals
    if game_array[0][0][2] == game_array[1][1][2] != '' and (game_array[2][2][2] == ''):
        return (2, 2)
    elif game_array[0][0][2] == game_array[2][2][2] != '' and (game_array[1][1][2] == ''):
        return (1, 1)
    elif game_array[1][1][2] == game_array[2][2][2] != '' and (game_array[0][0][2] == ''):
        return (0, 0)
    if game_array[0][2][2] == game_array[1][1][2] != '' and (game_array[2][0][2] == ''):
        return (2, 0)
    elif game_array[2][0][2] == game_array[1][1][2] != '' and (game_array[0][2][2] == ''):
        return (0, 2)
    elif game_array[0][2][2] == game_array[2][0][2] != '' and (game_array[1][1][2] == ''):
        return (1, 1)
    return -1


# Checking if someone has won
def has_won(game_array):
    # Checking rows
    for row in range(len(game_array)):
        if (game_array[row][0][2] == game_array[row][1][2] == game_array[row][2][2]) and game_array[row][2][2] != "":
            display_message(game_array[row][1][2].upper() + " has won")
            game_data["game_"+str(game_num)].update({'winner':game_array[row][1][2]})
            print(game_array[row][1][2] + ' has won')
            return True

    # Checking columns
    for col in range(len(game_array)):
        if (game_array[0][col][2] == game_array[1][col][2] == game_array[2][col][2]) and game_array[0][col][2] != "":
            display_message(game_array[0][col][2].upper() + " has won")
            game_data["game_"+str(game_num)].update({'winner':game_array[0][col][2]})
            print(game_array[0][col][2] + ' has won')
            return True

    # Checking main diagonal
    if (game_array[0][0][2] == game_array[1][1][2] == game_array[2][2][2]) and game_array[0][0][2] != "":
        display_message(game_array[0][0][2].upper() + " has won")
        game_data["game_"+str(game_num)].update({'winner':game_array[0][0][2]})
        print(game_array[0][0][2] + ' has won')
        return True

    # Checking reverse diagonal
    if (game_array[0][2][2] == game_array[1][1][2] == game_array[2][0][2]) and game_array[0][2][2] != "":
        display_message(game_array[0][2][2].upper() + " has won")
        game_data["game_"+str(game_num)].update({'winner':game_array[0][2][2]})
        print(game_array[0][2][2] + ' has won')
        return True

    return False

def has_drawn(game_array):
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            if game_array[i][j][2] == "":
                return False
    
    game_data["game_"+str(game_num)].update({'winner':'draw'})
    display_message("It's a tie")
    return True


def display_message(content):
    pygame.time.delay(500)
    win.fill(WHITE)
    end_text = END_FONT.render(content, 1, BLACK)
    win.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)


def render():
    win.fill(WHITE)
    draw_grid()

    # Drawing X's and O's
    for image in images:
        x, y, IMAGE = image
        win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

    pygame.display.update()


def main():
    global x_turn, o_turn, images, draw, game_array, run

    images = []
    draw = False

    run = True

    x_turn = True
    o_turn = False

    game_array = initialize_grid()

main()
render()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     #click(game_array)
        # if x_turn:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         click(game_array)
        #         move_num += 1
        # else:
    ai_counter(game_array, check_board(game_array))
    move_num += 1

    time.sleep(1)
    render()

    if has_won(game_array):
        run = False
    elif has_drawn(game_array):
        run = False


game_num += 1
#print(current_game)
m = open('game_data.json', 'w')
json.dump(game_data, m)
m.close()
f = open('store.pckl', 'wb')
pickle.dump(game_num, f)
f.close()