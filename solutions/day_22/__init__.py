from shared import main
from collections import deque
import itertools
import copy


def preprocess(data_input):
    players = data_input.strip().split('\n\n')
    decks = []
    for player in players:
        deck = deque([int(val) for val in player.strip().split('\n')[1:]])
        decks.append(deck)
    return decks[0], decks[1]


def play_round(deck0, deck1):
    play0 = deck0.popleft()
    play1 = deck1.popleft()
    if play0 > play1:
        deck0.append(play0)
        deck0.append(play1)
    else:
        deck1.append(play1)
        deck1.append(play0)


def play_game(deck0, deck1):
    while len(deck0) > 0 and len(deck1) > 0:
        play_round(deck0, deck1)
    if len(deck0) > 0:
        return calculate_win(deck0)
    return calculate_win(deck1)


def play_round_rec(deck0, deck1):
    play0 = deck0.popleft()
    play1 = deck1.popleft()
    if len(deck0) >= play0 and len(deck1) >= play1:
        new_deck0 = copy.deepcopy(deque(itertools.islice(deck0, 0, play0)))
        new_deck1 = copy.deepcopy(deque(itertools.islice(deck1, 0, play1)))
        player, deck = play_game_rec(new_deck0, new_deck1)
        if player == 0:
            deck0.append(play0)
            deck0.append(play1)
        else:
            deck1.append(play1)
            deck1.append(play0)
        return
    if play0 > play1:
        deck0.append(play0)
        deck0.append(play1)
    else:
        deck1.append(play1)
        deck1.append(play0)


def play_game_rec(deck0, deck1):
    previous_hands = []
    while len(deck0) > 0 and len(deck1) > 0:
        if check_previous_hands(deck0, deck1, previous_hands):
            return 0, deck0
        previous_hands.append((copy.deepcopy(deck0), copy.deepcopy(deck1)))
        play_round_rec(deck0, deck1)
    if len(deck0) > 0:
        return 0, deck0
    return 1, deck1


def check_previous_hands(deck0, deck1, previous_hands):
    for hand in previous_hands:
        if compare(deck0, hand[0]) and compare(deck1, hand[1]):
            return True
    return False


def compare(dq0, dq1):
    if len(dq0) != len(dq1):
        return False
    for i in range(len(dq0)):
        if dq0[i] != dq1[i]:
            return False
    return True


def calculate_win(deck):
    score = 0
    for i in range(len(deck)):
        score += (len(deck) - i) * deck[i]
    return score


def part1(data_input):
    deck0, deck1 = preprocess(data_input)
    return play_game(deck0, deck1)


def part2(data_input):
    deck0, deck1 = preprocess(data_input)
    player, deck = play_game_rec(deck0, deck1)
    return calculate_win(deck)


if __name__ == '__main__':
    main('input.txt', part1, part2)
