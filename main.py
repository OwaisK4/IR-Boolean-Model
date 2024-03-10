import os
import pickle
from preprocessor import Preprocessor
from indexer import InvertedIndex

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
            inverted_index.create_positional_index(preprocessor.tokens, filename)
        with open(saved_index, "wb") as f:
            pickle.dump(inverted_index, f)
        print("Created inverted index from scratch")

    print(f"Total tokens: {len(inverted_index.index)}")
    # with open("tokens", "w") as f:
    #     f.write(str(list(inverted_index.index.keys())))
    # posting = inverted_index.parse_query("artificial intelligence / 3")
    # posting.display() if posting is not None else print("NIL")
    # posting = inverted_index.parse_query("higher value / 2")
    # posting.display() if posting is not None else print("NIL")

    while True:
        query = input("Query: ")
        posting = inverted_index.parse_query(query)
        if posting == None:
            print("NIL")
        else:
            posting.display()
