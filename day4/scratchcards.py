def read_file(file):
    with open(file) as f:
        lines = f.readlines()

    deck = []
    for line in lines:
        fields = line.split(":")
        card = int(fields[0].split(" ")[-1])

        number_field = fields[1].strip("\n").split("|")
        winning_number = [int(n) for n in number_field[0].split(" ") if n.isnumeric()]
        number = [int(n) for n in number_field[1].split(" ") if n.isnumeric()]
        deck.append({"card" : card,
                     "winning_number" : winning_number,
                     "number" : number})
    return deck

def matches(number, winning):
    n = set(number)
    w = set(winning)
    match = set.intersection(n, w)
    return match

def calculate_score(number, winning):
    match = matches(number, winning)

    if not match:
        return 0

    score = 1
    for _ in list(match)[1:]:
        score *= 2

    return score

def sum_score(deck) :
    score = 0
    for card in deck:
        score += calculate_score(card["number"], card["winning_number"])
    return score

def calculate_number_of_cards(deck, n):
    n_cards = 0
    for i, card in enumerate(deck):
        # Limit number of cards to check
        if i == n :
            break
        # Add this card to the count
        n_cards += 1
        match = matches(card["number"], card["winning_number"])

        # Search recursive among new "copies"
        if match:
            n_cards += calculate_number_of_cards(deck[i + 1:], len(match))
    return n_cards


def main() :
    deck = read_file("day4/input")
    score = sum_score(deck)
    print(score)

    cards =calculate_number_of_cards(deck, len(deck))
    print(cards)


if __name__ == '__main__' :
    main()
