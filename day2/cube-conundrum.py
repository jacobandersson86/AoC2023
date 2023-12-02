colors = ["blue", "green", "red"]
bag = {"red" : 12, "green" :  13, "blue" : 14}

def is_possible_game(game, bag):
    for key in bag.keys():
        if bag[key] < game[key] :
            return False
    return True

def get_game(line) :
    id = line[5:].split(":")[0]
    game = {"id" : id}

    for color in colors:
        game[color] = 0

    line = line.split(":")[1]
    line = line[1:]

    words = line.strip(",").split(" ")
    numbers = words[0::2]
    input_colors = words[1::2]

    for number, color in zip(numbers, input_colors) :
        key = color.strip(";,\n")
        if game[key] < int(number) :
            game[key] = int(number)

    return game

def get_power(game) :
    value = 1
    for color in colors:
        value *= game[color]
    return value

def main():
    with open("day2/input") as f:
        lines = f.readlines()

    games = []
    removed = []
    powers = []
    for line in lines:
        game = get_game(line)
        if is_possible_game(game, bag) :
            games.append(game)
        else:
            removed.append(game)

        powers.append(get_power(game))

    print("Removed:")
    for game in removed:
        print(game)

    print("Kept:")
    for game in games:
        print(game)

    idx = [int(game["id"]) for game in games]
    print(f"Result 1: {sum(idx)}")

    print(f"Result 2: {sum(powers)}")

if __name__ == '__main__' :
    main()
