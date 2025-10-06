

def check_options(option, shot):
    if option == "double" and shot[0] == "D":
        return True
    elif option == "triple" and shot[0] == "T":
        return True
    elif option == "None":
        return True
    else:
        return False

def calculate_total_score(shots: list):
    total = 0
    for shot in shots:
        if shot[0] == "T":
            score = int(shot[1:])
            total += score*3
        elif shot[0] == "D":
            score = int(shot[1:])
            total += score * 2
        else:
            score = int(shot)
            total += score

    return total

def get_former_index(switching_next, index):
    from models.Game import Game
    last_index = Game.get_instance().nb_players -1
    if switching_next:
        return index + 1 if index < last_index else 0
    else:
        return index - 1 if index > 0 else last_index

