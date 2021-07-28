import pickle

first_call = True
f = open('store.pckl', 'rb')
while first_call:
    try:
        game_num = pickle.load(f)
        first_call = False
    except EOFError:
        game_num = 1
        first_call = False
 
print(game_num)
game_num += 1
f = open('store.pckl', 'wb')
pickle.dump(game_num, f)
f.close()

