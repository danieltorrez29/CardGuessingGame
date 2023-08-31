import random
import json
import time
import datetime


suits = ["♦", "♣", "♠"]
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

players = []


def create_card_deck():
    """Function that is responsible for creating a deck of cards.

    Returns:
        list[]: list of tuples
    """
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append((rank, suit))
    return deck


def get_three_cards():
    """Function that takes three cards: two random cards and a queen of hearts.

    Returns:
        list[]: list of tuples
    """
    card_deck = create_card_deck()
    shuffled_cards = []
    shuffled_cards.append(("Q", "♥"))
    for i in range(2):
        shuffled_cards.append(card_deck[random.randint(0, len(card_deck) - 1)])
    random.shuffle(shuffled_cards)
    return shuffled_cards


def print_cards(cards):
    """Function that is responsible for displaying cards graphically using ASCII art.

    Args:
        cards (list[]): cards
    """
    card_art = [" ______ ", "|{}    |", "|  {}  |", "|    {}|", " ------ "]

    for i in range(5):
        row = ""
        for suit, rank in cards:
            if i == 1 or i == 3:
                row += card_art[i].format(suit.center(2))
            elif i == 2:
                row += card_art[i].format(rank.center(2))
            else:
                row += card_art[i]
        print(row)


def swap_cards(cards):
    """Function that is responsible for swapping two random cards, showing only the positions of the cards involved and creating a random execution delay.

    Args:
        cards (list[]): cards

    Returns:
        list[]: list of tuples
    """
    first_card_index = random.randint(0, 2)
    second_card_index = random.randint(0, 2)
    flag = True
    while flag:
        if first_card_index == second_card_index:
            second_card_index = random.randint(0, 2)
        else:
            flag = False
    swapped_cards = cards.copy()
    swapped_cards[first_card_index] = cards[second_card_index]
    swapped_cards[second_card_index] = cards[first_card_index]
    message = "Intercambio "
    if first_card_index == 0:
        message += "izquierda (I) con "
    elif first_card_index == 1:
        message += "la del medio (M) con "
    else:
        message += "derecha (D) con "

    if second_card_index == 0:
        message += "izquierda (I)"
    elif second_card_index == 1:
        message += "la del medio (M)"
    else:
        message += "derecha (D)"
    print(message + "...")
    delay = random.uniform(0.5, 2.0)
    time.sleep(delay)
    return swapped_cards


class Player:
    """Class representing a player."""

    def __init__(self, name, points, best_play):
        """Constructor.

        Args:
            name (string): player's name
            points (int): player's points
            best_play (string): player's best play
        """
        self.name = name
        self.points = points
        self.best_play = best_play

    def update_points(self, points):
        """Function that is responsible for updating points.

        Args:
            points (int): game points
        """
        self.points = points

    def update_best_play(self, play):
        """Function that is responsible for updating best play.

        Args:
            play (string): game best play
        """
        self.best_play = play

    def __str__(self):
        """Player's to string.

        Returns:
            string: string attributes
        """
        return (
            f"Player: {self.name}\nPoints: {self.points}\nBest play: {self.best_play}"
        )


def read_players():
    """Function that is responsible for reading the list of players from a JSON file and sets the list of type Player."""
    with open("players.json", "r") as json_file:
        data = json.load(json_file)
    global players
    players_aux = []
    for player_data in data:
        player = Player(
            player_data["name"], player_data["points"], player_data["best_play"]
        )
        players_aux.append(player)
    players = players_aux


def write_players():
    """Function that is responsible for writing the list of players in a JSON file."""
    json_list = []
    for player in players:
        player_dict = {
            "name": player.name,
            "points": player.points,
            "best_play": player.best_play,
        }
        json_list.append(player_dict)

    with open("players.json", "w") as file:
        json.dump(json_list, file, indent=4)


def sort_players():
    """Function that is responsible of ordering the list of players in descending order depending on their score."""
    global players
    players = sorted(players.copy(), key=lambda player: player.points, reverse=True)


def search_player(name):
    """Function that is responsible for searching for a player by name in the list of players.

    Args:
        name (string): player's name

    Returns:
        Player: searched player
    """
    for player in players:
        if player.name.lower() == name.lower():
            return player
    return None


def is_right_guess_position(guess, cards):
    """Function that determines if given three cards, the card chosen by the player is the queen of hearts.

    Args:
        guess (string): card position
        cards (list[]): list of tuples

    Returns:
        bool: True -> Got it right | False -> Failed
    """
    flag = False
    if guess == "I":
        if cards[0][1] == "♥":
            flag = True
    elif guess == "M":
        if cards[1][1] == "♥":
            flag = True
    else:
        if cards[2][1] == "♥":
            flag = True
    return flag


def get_best_play_message():
    """Function that gets the best play message according to the current date and time.

    Returns:
        string: best play message
    """
    return (
        "Mejor jugada el "
        + str(datetime.datetime.now().date())
        + " a las "
        + str(datetime.datetime.now().time().strftime("%I:%M %p"))
    )


def main():
    """Function with all the logic of the guessing game."""
    while True:
        read_players()
        option = input(
            "\nAdivina dónde está la reina de corazones\n\n> Seleccione: jugar [J], tabla de posiciones [T], salir [S]: "
        )
        if option.upper() == "J":
            cards = get_three_cards()
            player_name = input("Por favor ingrese su nombre: ")
            player_name = player_name.capitalize()
            player_points = 0
            current_player = search_player(player_name)
            flag = True
            print(
                f"\n¡{player_name} mantén tus ojos abiertos mientras las cartas se mueven!"
            )
            print_cards(cards)
            input("Presiona ENTER cuando estés listo(a): ")
            print("")
            while flag:
                swaps = random.randint(5, 8)
                for i in range(swaps):
                    cards = swap_cards(cards)
                guess = input(
                    "\n¿En cuál de las cartas está la reina de corazones? [I], [M], [D]: "
                )
                guess = guess.upper()
                if is_right_guess_position(guess, cards):
                    player_points += 1
                    print_cards(cards)
                    print("\n¡Acertaste!\n")
                else:
                    flag = False
                    print_cards(cards)
                    print("\nLo siento perdedor(a) :-(\n¡Gracias por jugar!")
            if current_player != None:
                if current_player.points < player_points:
                    current_player.update_points(player_points)
                    current_player.update_best_play(get_best_play_message())
                    write_players()
            else:
                players.append(
                    Player(
                        player_name,
                        player_points,
                        get_best_play_message(),
                    )
                )
                write_players()
        elif option.upper() == "T":
            sort_players()
            print("\nTop 5 de lo(a)s mejores:\n")
            for i in range(5):
                print(
                    f"{i+1}. {players[i].name}, {players[i].points} puntos. {players[i].best_play}"
                )
        elif option.upper() == "S":
            print("\n¡Adiós!")
            break
        else:
            print("\nOpción no válida. Por favor, seleccione una opción válida.")


if __name__ == "__main__":
    """__name__: used to determine if a Python file is being executed as a main program or if it is being imported as a module in another program.
    if __name__ == "__main__": used to check if the current file is being executed directly as a main program. If so, the code inside this block will be executed.
    """
    main()
