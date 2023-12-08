from functools import cmp_to_key
from itertools import permutations
from enum import IntEnum
from math import factorial
import time
import random

class scores(IntEnum):
    FIVE_OF_A_KIND = 21
    FOUR_OF_A_KIND = 20
    FULL_HOUSE = 19
    THREE_OF_A_KIND = 18
    TWO_PAIRS = 17
    ONE_PAIR = 16
    HIGH_CARD = 15


card_value = {
    "A" : 14,
    "K" : 13,
    "Q" : 12,
    "T" : 11,
    "9" : 10,
    "8" : 8,
    "7" : 7,
    "6" : 6,
    "5" : 5,
    "4" : 4,
    "3" : 3,
    "2" : 2,
    "J" : 1,
}

# This list is the reverse order of what I expect the sorted to be.
manual_example = [
    ["JJAJJ", 0],
    ["JJJJJ", 0],
    # All of these have full house
    ["AAKKA", 0],
    ["AJKKA", 0],
    ["KAKKA", 0],
    ["JAKKA", 0],
    # # All of these have two pair
    ["QAKKA", 0],
    ["TKAKA", 0],
    ["9AKKA", 0],
    ["8AKKA", 0],
    ["7AKKA", 0],
    ["6AKKA", 0],
    ["5AKKA", 0],
    ["4AKKA", 0],
    ["3AKKA", 0],
    # # All of these have one pair
    ["AQ7KA", 0],
    ["A27KA", 0],
    ["AJ8K7", 0],
    ["JA8K7", 0],
]

tests = [
    # Five of a kind, where all five cards have the same label: AAAAA
    ["AAAAA", scores.FIVE_OF_A_KIND],
    ["TTTTT", scores.FIVE_OF_A_KIND],
    ["J2222", scores.FIVE_OF_A_KIND],
    ["JJTTT", scores.FIVE_OF_A_KIND],
    ["JJJTT", scores.FIVE_OF_A_KIND],
    ["JJJJT", scores.FIVE_OF_A_KIND],
    ["JJJJJ", scores.FIVE_OF_A_KIND],
    # Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    ["AA8AA", scores.FOUR_OF_A_KIND],
    ["3TTTT", scores.FOUR_OF_A_KIND],
    ["3JTTT", scores.FOUR_OF_A_KIND],
    ["3J2JJ", scores.FOUR_OF_A_KIND],
    ["332JJ", scores.FOUR_OF_A_KIND],
    # Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    ["23332", scores.FULL_HOUSE],
    ["AAQAQ", scores.FULL_HOUSE],
    ["AJQAQ", scores.FULL_HOUSE],
    ["332J2", scores.FULL_HOUSE],
    # Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    ["TTT98", scores.THREE_OF_A_KIND],
    ["33732", scores.THREE_OF_A_KIND],
    ["3122J", scores.THREE_OF_A_KIND],
    ["312JJ", scores.THREE_OF_A_KIND],
    # Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    ["23432", scores.TWO_PAIRS],
    ["ATQTA", scores.TWO_PAIRS],
    ["73722", scores.TWO_PAIRS],
    # One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    ["A23A4", scores.ONE_PAIR],
    ["32T3K", scores.ONE_PAIR],
    ["ATQ3A", scores.ONE_PAIR],
    ["AT8QJ", scores.ONE_PAIR],
    # High card, where all cards' labels are distinct: 23456
    ["23456", scores.HIGH_CARD],
    ["5A3TQ", scores.HIGH_CARD],
    # With Jacks
    # Impossible to get two pair with one J, you should use it for a three of a kind
    # Impossible to get high hand with one J, you should use it for a pair
]

def read_file(file):
    with open(file) as f :
        lines = f.readlines()

    deck = []
    for line in lines:
        hand, bid = line.strip("\n").split(" ")
        deck.append({"hand" : hand, "bid" : int(bid)})
    return deck

def score(hand) -> scores:
    unique_cards = set([*hand])
    n_unique = len(unique_cards)

    n_J = 0
    if "J" in unique_cards:
        n_J = hand.count("J")
        n_unique -= 1
        if n_unique == 0:
            return scores.FIVE_OF_A_KIND

    if n_unique == 1 :
        return scores.FIVE_OF_A_KIND

    most_of_one = 0
    if "J" in unique_cards:
        unique_cards.remove("J")
    for card in unique_cards :
        n_card = hand.count(card) + n_J
        if n_card > most_of_one :
            most_of_one = n_card

    if n_unique == 2 :
        if most_of_one == 4 :
            # Four of a kind
            return scores.FOUR_OF_A_KIND
        # Full house
        return scores.FULL_HOUSE
    if n_unique == 3 :
        if most_of_one == 3 :
            # Three of a kind
            return scores.THREE_OF_A_KIND
        # Two pair
        return scores.TWO_PAIRS

    if n_unique == 4 :
        # One pair
        return scores.ONE_PAIR

    # High Hand
    return scores.HIGH_CARD

def compare(item1, item2):
    score1 = score(item1["hand"])
    score2 = score(item2["hand"])

    value = score1 - score2

    if value == 0 :
        for c1, c2 in zip([*item1["hand"]], [*item2["hand"]]) :
            v1 = card_value[c1]
            v2 = card_value[c2]
            if v1 == v2 :
                continue
            return v1 - v2
        print(f"item1 {item1} item2 {item2}")
        raise ValueError

    return value

def main():
    test_deck = []
    manual_deck = []
    for hand, bid in manual_example:
        test_deck.append({"hand" : hand, "bid" : int(bid)})
        manual_deck.append({"hand" : hand, "bid" : int(bid)})

    all_permutations = [manual_deck] # permutations(manual_deck)
    n_perm = factorial(len(manual_deck))

    for i, permutation in enumerate(all_permutations):
        # if i % 100000 == 0:
        #     print(f"Still searching... {i} of {n_perm}")
        sorted_test_deck = sorted(permutation, key=cmp_to_key(compare))
        for sorted_card, manual_card in zip(sorted_test_deck, reversed(manual_deck)):
            if sorted_card["hand"] != manual_card["hand"] :
                raise Exception(f"Different hands! {sorted_card['hand']} vs. {manual_card['hand']}")

    for hand, s in tests:
        if s != score(hand):
            raise Exception(f"Score of hand {hand} is {str(score(hand))} expected {s}")

    deck = read_file("day7/input")
    deck = sorted(deck, key = cmp_to_key(compare))

    total = 0
    for i, item in enumerate(deck):
        total += (i + 1) * item["bid"]

    if total == 251296863 :
        raise ValueError(f"251296863 is not correct!")
    print(total)

if __name__ == '__main__' :
    main()
