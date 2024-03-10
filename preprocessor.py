import re
import nltk
from string import ascii_letters, digits


class Preprocessor:
    def __init__(self, filepath: str = None) -> None:
        self.raw_text: str = open(filepath, "r", encoding="cp1252").read()
        self.delimiters = [" ", "_", "-", ",", "|", ";", ":", "!", "?"]
        self.raw_tokens: list[str] = self.raw_text.split()
        for delim in self.delimiters:
            self.raw_tokens = " ".join(self.raw_tokens).split(delim)
        self.raw_tokens = " ".join(self.raw_tokens).split()
        self.tokens: list[tuple[str, int]] = []
        # self.alphanumeric = ascii_letters + digit
        self.alphabet = ascii_letters
        self.stop_words = [
            "a",
            "is",
            "the",
            "of",
            "all",
            "and",
            "to",
            "can",
            "be",
            "as",
            "once",
            "for",
            "at",
            "am",
            "are",
            "has",
            "have",
            "had",
            "up",
            "his",
            "her",
            "in",
            "on",
            "no",
            "we",
            "do",
        ]

    def print_raw(self) -> None:
        print(self.raw_text)

    def clean_tokens(self):
        stemmer = nltk.PorterStemmer()
        i = 0
        for token in self.raw_tokens:
            token = token.strip()
            token = token.lower()
            for char in token:
                if char not in self.alphabet:
                    token = token.replace(char, "")
            if token != "" and token not in self.stop_words and len(token) > 2:
                token = stemmer.stem(token)
                self.tokens.append((token, i))
            i += 1

    def process(self):
        self.clean_tokens()
