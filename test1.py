game_num = 1
game_data1 = {"game_"+str(game_num):{}}
game_data2 = {"move_1": {"char":"x","coords":"(1, 2)"}}
game_data3 = {"move_2": {"char":"o","coords":"(1, 1)"}}

game = game_data2|game_data3
print(game)
game_data1["game_"+str(game_num)].update(game)

print(game_data1)