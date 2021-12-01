def part1(player1: list, player2: list):
    while len(player1) != 0 and len(player2) != 0:
        card1 = player1.pop(0)
        card2 = player2.pop(0)

        if card1 > card2:
            player1.append(card1)
            player1.append(card2)
        else:
            player2.append(card2)
            player2.append(card1)

    deck = player1 if len(player2) == 0 else player2
    score = 0
    for i in range(len(deck)):
        score += (len(deck) - i) * deck[i]

    print(score)


def part2(player1: list, player2: list):
    game(player1, player2)

    deck = player1 if len(player2) == 0 else player2
    score = 0
    for i in range(len(deck)):
        score += (len(deck) - i) * deck[i]

    print(score)


def game(player1: list, player2: list):
    # Play the game until one deck of cards is empty. A memory is used to remember the match-ups which appeared in the
    # game. This will return True if player1 won, and False if player 2 won
    memory = []
    while len(player1) != 0 and len(player2) != 0:
        if combat_round(player1, player2, memory):
            return True

    return True if len(player2) == 0 else False


def combat_round(player1: list, player2: list, memory: list):
    # if the match-up was already present in this game, player 1 wins
    if (player1, player2) in memory:
        return True
    memory.append((player1[:], player2[:]))

    card1 = player1.pop(0)
    card2 = player2.pop(0)

    # sub-game is played if both players have as many cards as the card they drew
    if len(player1) >= card1 and len(player2) >= card2:
        if game(player1[:card1], player2[:card2]):
            player1.append(card1)
            player1.append(card2)
        else:
            player2.append(card2)
            player2.append(card1)
    else:
        # no sub-game could be played, so highest card wins
        if card1 > card2:
            player1.append(card1)
            player1.append(card2)
        else:
            player2.append(card2)
            player2.append(card1)


# read in starting cards
with open("input.txt", "r") as file:
    cards = [player_cards for player_cards in file.read().split("\n\n")]

player_cards1 = [int(i) for i in cards[0].split("\n")[1:]]
player_cards2 = [int(i) for i in cards[1].split("\n")[1:]]
part1(player_cards1, player_cards2)

player_cards1 = [int(i) for i in cards[0].split("\n")[1:]]
player_cards2 = [int(i) for i in cards[1].split("\n")[1:]]
part2(player_cards1, player_cards2)
