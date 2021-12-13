from collections import Counter, defaultdict
from random import choice

import nltk


class TextGenerator:
    def __init__(self):
        self.file = None
        self.tokens = None
        self.bigrams = None
        self.trigrams = None
        self.markov_chain = defaultdict(lambda _: Counter())
        self.markov_chain_with_trigrams = {}

    def app_start(self):
        self.load_file()
        self.do_sixth_task()

    def load_file(self):
        file_name = input()
        # file_name = "corpus.txt"
        with open(file=file_name, mode="r", encoding="utf-8") as file:
            self.file = file.read()

    def check_user_input(self, task_print):
        while True:
            user_input = input()
            if user_input == "exit":
                break
            try:
                index = int(user_input)
            except ValueError:
                print("Type Error. Please input an integer.")
                continue
            task_print(index)

    def get_bigrams(self):
        self.tokens = nltk.WhitespaceTokenizer().tokenize(self.file)
        self.bigrams = tuple(nltk.bigrams(self.tokens))

    def get_trigrams(self):
        self.tokens = nltk.WhitespaceTokenizer().tokenize(self.file)
        self.trigrams = tuple(nltk.trigrams(self.tokens))

    def get_markov_chain(self):
        for head, tail in self.bigrams:
            if head not in self.markov_chain:
                self.markov_chain[head] = Counter()
            self.markov_chain[head][tail] += 1

    def do_first_task(self):
        tokenizer = nltk.WhitespaceTokenizer()
        self.tokens = tokenizer.tokenize(self.file)
        self.first_task_print_statistics()
        self.check_user_input(task_print=self.first_task_print)

    def first_task_print(self, index):
        try:
            print(self.tokens[index])
        except IndexError:
            print(
                "Index Error. Please input an integer that is in the range of the corpus."
            )

    def first_task_print_statistics(self):
        print("Corpus statistics")
        print(f"All tokens: {len(self.tokens)}")
        print(f"Unique tokens: {len(set(self.tokens))}")

    def do_second_task(self):
        self.get_bigrams()
        print(f"Number of bigrams: {len(self.bigrams)}")
        self.check_user_input(task_print=self.second_task_print)

    def second_task_print(self, index):
        try:
            head, tail = self.bigrams[index]
            print(f"Head: {head} Tail: {tail}")
        except IndexError:
            print(
                "Index Error. Please input a value that is not greater than the number of all bigrams."
            )

    def do_third_task(self):
        self.get_bigrams()
        self.get_markov_chain()
        self.third_task_user_input()

    def third_task_user_input(self):
        while True:
            user_input = input()
            if user_input == "exit":
                break
            print(f"Head: {user_input}")
            if user_input in self.markov_chain:
                for tail, tail_count in sorted(
                    self.markov_chain[user_input].items(),
                    key=lambda i: i[1],
                    reverse=True,
                ):
                    print(f"Tail: {tail} Count: {tail_count}")
            else:
                print(
                    "Key Error. The requested word is not in the model. Please input another word."
                )

    def do_fourth_task(self):
        self.get_bigrams()
        self.get_markov_chain()
        sentences_number = 10
        generated_text = self.generate_strict_random_sentences(
            sentences_number=sentences_number
        )
        print(generated_text)

    def generate_strict_random_sentences(
        self, sentences_number: int = 10, words_in_sentence: int = 5
    ):
        text = []
        words = tuple(self.markov_chain.keys())
        while len(text) != sentences_number:
            sentence = []
            for _ in range(words_in_sentence):
                head = choice(words)
                tail, _ = sorted(
                    self.markov_chain[head].items(), key=lambda i: i[1], reverse=True
                )[0]
                sentence.append(f"{head} {tail}")
            text.append(" ".join(sentence))
        return "\n".join(text)

    def do_fifth_task(self):
        self.get_bigrams()
        self.get_markov_chain()
        generated_text = self.generate_full_sentences()
        print(generated_text)

    def generate_full_sentences(
        self, sentences_number: int = 10, words_in_sentence: int = 10
    ):
        text = []
        words = tuple(self.markov_chain.keys())
        while len(text) != sentences_number:
            sentence = []
            head = self.get_first_word(words=words)
            sentence.append(head)
            while True:
                end_sentence = False
                for tail, _ in sorted(
                    self.markov_chain[head].items(), key=lambda i: i[1], reverse=True
                ):
                    if len(sentence) >= words_in_sentence and tail[-1] in ".!?":
                        end_sentence = True
                        break
                    if tail != head and tail[-1] not in ".!?":
                        break
                sentence.append(tail)
                head = tail

                if end_sentence:
                    break
            text.append(" ".join(sentence))
        return "\n".join(text)

    def get_first_word(self, words: tuple):
        while True:
            word = choice(words)
            if word[0].isupper() and word[-1] not in ",.!?":
                return word

    def do_sixth_task(self):
        self.get_trigrams()
        self.get_markov_chain_with_trigrams()
        text = self.generate_full_sentences_with_trigrams()
        print(text)

    def get_markov_chain_with_trigrams(self):
        for head, middle, tail in self.trigrams:
            key = f"{head} {middle}"
            if key not in self.markov_chain:
                self.markov_chain[key] = Counter()
            self.markov_chain[key][tail] += 1

    def generate_full_sentences_with_trigrams(
        self, sentences_number: int = 10, words_in_sentence: int = 5
    ):
        text = []
        words = tuple(self.markov_chain.keys())
        while len(text) != sentences_number:
            sentence = []
            # head = None
            while True:
                word = choice(words)
                if word[0].isupper() and word.split()[0][-1] not in ",.!?":
                    break
            head = word
            sentence.append(head)
            while True:
                end_sentence = False
                for tail, _ in sorted(
                    self.markov_chain[head].items(), key=lambda i: i[1], reverse=True
                ):
                    if len(sentence) >= words_in_sentence and tail[-1] in ".!?":
                        end_sentence = True
                        break
                    if tail != head and tail[-1] not in ".!?":
                        break
                sentence.append(tail)
                head = f"{head.split()[-1]} {tail}"

                if end_sentence:
                    break
            text.append(" ".join(sentence))
        return "\n".join(text)


if __name__ == "__main__":
    text_generator = TextGenerator()
    text_generator.app_start()
