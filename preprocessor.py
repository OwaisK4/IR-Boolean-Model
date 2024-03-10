import nltk
from string import ascii_letters

"""
Preprocessor class that processes each token.
It works as follows:
1. Read the raw text from file using cp1252 encoding (Because the given documents contain some Latin-1 characters).
2. Tokenize them using multiple delimiters (i.e. self.delimiters).
3. Clean the tokens i.e. casefold, strip whitespace and remove all digits and punctuation.
4. Stem the tokens using Porter Stemmer imported from nltk library.
5. Store the cleaned tokens in self.tokens.
"""


class Preprocessor:
    def __init__(self, filepath: str = None) -> None:
        self.raw_text: str = open(filepath, "r", encoding="cp1252").read()
        self.delimiters = [" ", "_", "-", ",", "|", ";", ":", "!", "?"]
        self.raw_tokens: list[str] = self.raw_text.split()
        for delim in self.delimiters:
            self.raw_tokens = " ".join(self.raw_tokens).split(delim)
        self.raw_tokens = " ".join(self.raw_tokens).split()
        self.tokens: list[tuple[str, int]] = []
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
