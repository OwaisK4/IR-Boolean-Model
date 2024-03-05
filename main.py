import os
from preprocessor import Preprocessor
from indexer import InvertedIndex

# from random import randint

filepath = "/home/owaisk4/Win_backup/FAST NU assignments/Information Retrieval/Assignment 1/ResearchPapers"

if __name__ == "__main__":
    inverted_index = InvertedIndex()

    files = os.listdir(filepath)
    files = [os.path.join(filepath, file) for file in files]

    for file in files:
        filename = int(file.split("/")[-1].split(".")[0])
        preprocessor = Preprocessor(file)
        preprocessor.process()
        inverted_index.create_index(preprocessor.tokens, filename)

    posting = inverted_index.AND_query("transformer", "model")
    posting.display()
    posting = inverted_index.AND_query("cancer", "learning")
    posting.display()
    posting = inverted_index.AND_query("cancer", "learning")
    posting.display()
