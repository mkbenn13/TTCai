import json

game_data = json.load(open('game_data.json'))
cur ={
    "game_1": {
        "move_1": {
            "char": "x",
            "coords": "(249, 415)"
        },
        "move_2": {
            "char": "o",
            "coords": "(415, 83)"
        },
        "move_3": {
            "char": "x",
            "coords": "(415, 249)"
        },
        "move_4": {
            "char": "o",
            "coords": "(83, 415)"
        },
        "move_5": {
            "char": "x",
            "coords": "(415, 415)"
        },
        "move_6": {
            "char": "o",
            "coords": "(249, 249)"
        },
        "winner": "o"
    }
}

# for game in game_data:
#     #{k: game[k] for k in game if k in cur and game[k] == cur[k]}
#     for move in game_data[game]: 
#         for key, value in game_data[game][move].items():
#             if value in cur[game][move] and game[move] == cur[move]:
#                 print(j)

current_char = 'x'

for game, value in game_data.items():
    for move, value2 in game_data[game].items():
        if move == 'winner':
            break
        for char, value3 in value[move].items():
            if value3 == current_char and current_char == game_data[game]['winner']:
                print('hi')


# print(game_data['game_1']['move_1']['char'])
# print(cur)


