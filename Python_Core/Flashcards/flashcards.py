import argparse
import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


@dataclass()
class Card:
    term: str
    definition: str
    errors: int = 0
    checked: bool = False


class Flashcard:

    def __init__(self, import_from: str = "", export_to: str = "") -> None:
        self.cards: List[Card] = []
        self.terms = set()
        self.definitions = set()
        self.logs = []
        self.menu = {
            "add": self.add_card,
            "remove": self.remove_card,
            "import": self.import_cards,
            "export": self.export_cards,
            "ask": self.check_cards,
            "exit": self.close_app,
            "log": self.log,
            "hardest card": self.get_hardest_card,
            "reset stats": self.reset_stats
        }
        if import_from:
            self.import_cards(file_name=import_from)
        self.export_to = export_to

    def start_app(self):
        user_input = ""
        while user_input != "exit":
            user_input = input(
                self._add_log_line(
                    "Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n"))
            if user_input in self.menu:
                self.menu[user_input]()

    def close_app(self):
        if self.export_to:
            self.export_cards(file_name=self.export_to)
        print(self._add_log_line("Bye bye!"))

    def reset_stats(self):
        for position in range(len(self.cards)):
            self.cards[position].errors = 0
        print(self._add_log_line('Card statistics have been reset.\n'))

    def _add_log_line(self, line: str) -> str:
        self.logs.append(line.strip())
        return line

    def log(self):
        file_name = input('File name:\n')
        with open(file_name, mode="a+", encoding="utf-8") as file:
            file.write("\n".join((line for line in self.logs)))
        print(self._add_log_line("The log has been saved."))

    def get_hardest_card(self):
        max_errors = max(card.errors for card in self.cards) if self.cards else 0
        if max_errors == 0:
            print(self._add_log_line("There are no cards with errors."))
            return
        cards_with_max_errors = [card for card in self.cards if card.errors == max_errors]
        if len(cards_with_max_errors) == 1:
            print(self._add_log_line(
                f'The hardest card is "{cards_with_max_errors[0].term}". You have {cards_with_max_errors[0].errors} errors answering it.'))
        else:
            print(self._add_log_line(
                f"""The hardest cards are {', '.join((f'"{card.term}"' for card in cards_with_max_errors))}."""))

    def remove_card(self):
        term = input(self._add_log_line(f"Which card?\n"))
        if term not in self.terms:
            print(self._add_log_line(f"""Can't remove "{term}": there is no such card."""))
        else:
            position = self._get_card_position_by_term(term=term)
            if position is not None:
                self.terms.remove(term)
                id_card_for_del = self._get_card_position_by_term(term=term)
                self.definitions.remove(self.cards[id_card_for_del].definition)

                del self.cards[id_card_for_del]

                print(self._add_log_line("The card has been removed."))

    def import_cards(self, file_name: Optional[str] = None):
        if file_name is None:
            file_name = input('File name:\n')
        if not Path(file_name).is_file():
            print(self._add_log_line("File not found."))
            return
        imported_cards = []
        with open(Path(file_name), mode="r", encoding="utf-8") as file:
            lines = file.readlines()
            for line_number in range(0, len(lines), 3):
                imported_cards.append(Card(
                    term=lines[line_number].rstrip("\n"),
                    definition=lines[line_number + 1].rstrip("\n"),
                    errors=int(lines[line_number + 2].rstrip("\n")))
                )
        imported_count = 0
        for imported_card in imported_cards:

            if imported_card.term not in self.terms:
                self.cards.append(imported_card)
                self.terms.add(imported_card.term)
                self.definitions.add(imported_card.definition)
                imported_count += 1
            else:
                position = self._get_card_position_by_term(term=imported_card.term)
                self.cards[position] = imported_card
                imported_count += 1
        print(self._add_log_line(f"{imported_count} cards have been loaded."))

    def _get_card_position_by_term(self, term) -> Optional[int]:
        for card_position, card in enumerate(self.cards):
            if term == card.term:
                return card_position

    def export_cards(self, file_name: Optional[str] = None):

        if file_name is None:
            file_name = input(self._add_log_line('File name:\n'))

        with open(Path(file_name), mode="w", encoding="utf-8") as file:
            cards_text = "\n".join((
                f"{card.term}\n{card.definition}\n{card.errors}" for card in self.cards
            ))
            file.write(cards_text)
        print(self._add_log_line(f"{len(self.cards)} cards have been saved"))

    def _add_card(self, term, definition):
        self.cards.append(
            Card(term=term,
                 definition=definition))
        self.terms.add(term)
        self.definitions.add(definition)

    def add_card(self):
        term = input(self._add_log_line(f"The card:\n"))
        while term in self.terms:
            term = input(self._add_log_line(f'The card "{term}" already exists. Try again:\n'))
        definition = input(self._add_log_line(f"The definition of the card:\n"))
        while definition in self.definitions:
            definition = input(self._add_log_line(f'The definition "{definition}" already exists. Try again:\n'))
        self._add_card(
            term=term,
            definition=definition,
        )
        print(self._add_log_line(f""""The pair ("{term}":"{definition}") has been added."""))

    def _get_card_by_definition(self, definition: str) -> Optional[Card]:
        for card in self.cards:
            if card.definition == definition:
                return card

    def check_cards(self):
        cards_for_check = int(input(self._add_log_line("How many times to ask?\n")))
        checked = 0
        for card in itertools.cycle(self.cards):
            checked += 1
            if cards_for_check < checked:
                break
            user_input: str = input(self._add_log_line(f'Print the definition of "{card.term}":\n'))
            if user_input == card.definition:
                print(self._add_log_line("Correct!"))
                continue
            if user_input not in self.definitions:
                print(self._add_log_line(f'Wrong. The right answer is "{card.definition}".'))
            else:
                card_by_definition = self._get_card_by_definition(definition=user_input)
                print(self._add_log_line(
                    f'Wrong. The right answer is "{card.definition}", but your definition is correct for "{card_by_definition.term}".'))
            self.cards[self._get_card_position_by_term(term=card.term)].errors += 1

    def check_user_input(self, user_input: str, definition: str) -> Tuple[bool, Optional[Card]]:
        check = user_input == definition
        if check is False:
            for card in self.cards:
                if user_input == card.definition:
                    return check, card
        return check, None


class FlashcardArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="This ia a flashcard project for JB Academy")
        self.parser.add_argument("--import_from", default=None,
                                 help="File for loading")
        self.parser.add_argument("--export_to", default=None,
                                 help="File for export")
        self.parse_args()

    def parse_args(self) -> Tuple[Optional[str], Optional[str]]:
        args = self.parser.parse_args()
        return args.import_from, args.export_to


def main():
    import_from, export_to = FlashcardArgParser().parse_args()
    flashcard = Flashcard(import_from=import_from, export_to=export_to)
    flashcard.start_app()


if __name__ == '__main__':
    main()
