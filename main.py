import os
import pickle
from preprocessor import Preprocessor
from indexer import InvertedIndex

# from random import randint

filepath = "/home/owaisk4/Win_backup/FAST NU assignments/Information Retrieval/Assignment 1/ResearchPapers"
saved_index = os.path.join(filepath, "inverted_index.pkl")

if __name__ == "__main__":
    inverted_index = InvertedIndex()

    if os.path.exists(saved_index):
        with open(saved_index, "rb") as f:
            inverted_index = pickle.load(f)
        print("Loaded inverted index from file")

    else:
        files = os.listdir(filepath)
        files = [os.path.join(filepath, file) for file in files]

        for file in files:
            filename = int(file.split("/")[-1].split(".")[0])
            preprocessor = Preprocessor(file)
            preprocessor.process()
            inverted_index.create_index(preprocessor.tokens, filename)
        with open(saved_index, "wb") as f:
            pickle.dump(inverted_index, f)
        print("Created inverted index from scratch")

    posting = inverted_index.parse_query("transformer AND model")
    posting.display() if posting is not None else print("NIL")
    posting = inverted_index.parse_query("cancer AND learning")
    posting.display() if posting is not None else print("NIL")
    posting = inverted_index.parse_query("NOT agent OR agent")
    posting.display() if posting is not None else print("NIL")
    posting = inverted_index.parse_query(
        "aas AND owais OR cancer AND disease OR doctor"
    )
    posting.display() if posting is not None else print("NIL")
