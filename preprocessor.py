import nltk
from string import ascii_letters, digits


class Preprocessor:
    def __init__(self, filepath: str = None) -> None:
        assert filepath is not None
        self.filepath: str = filepath
        self.raw_text: str = open(self.filepath, "r", encoding="cp1252").read()
        self.raw_tokens: list[str] = nltk.word_tokenize(self.raw_text)
        self.tokens: list[str] = []
        self.alphanumeric = ascii_letters + digits
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
        for token in self.raw_tokens:
            token = token.strip()
            token = token.lower()
            for char in token:
                if char not in self.alphanumeric:
                    token = token.replace(char, "")
            if token != "" and not token.isdigit():
                for i in range(0, 10):
                    token = token.replace(str(i), "")
            if token != "" and token not in self.stop_words:
                self.tokens.append(token)

    def stem_tokens(self):
        stemmer = nltk.PorterStemmer()
        for i in range(0, len(self.tokens)):
            self.tokens[i] = stemmer.stem(self.tokens[i])

    def process(self):
        self.clean_tokens()
        self.stem_tokens()
        self.tokens = list(set(self.tokens))  # To remove duplicates
