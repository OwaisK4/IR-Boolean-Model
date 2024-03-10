import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QShortcut,
)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
import os
import pickle
from preprocessor import Preprocessor
from indexer import InvertedIndex


filepath = "/home/owaisk4/Win_backup/FAST NU assignments/Information Retrieval/Assignment 1/ResearchPapers"
saved_index = os.path.join(filepath, "inverted_index.pkl")

if __name__ == "__main__":
    inverted_index = InvertedIndex()

    # This condition will load the positional index from disk if it already exists.
    if os.path.exists(saved_index):
        with open(saved_index, "rb") as f:
            inverted_index = pickle.load(f)
        print("Loaded inverted index from file")

    # Otherwise, create a new positional index from scratch.
    else:
        files = os.listdir(filepath)
        files = [os.path.join(filepath, file) for file in files]
        for file in files:
            filename = int(file.split("/")[-1].split(".")[0])
            preprocessor = Preprocessor(file)
            preprocessor.clean_tokens()
            inverted_index.create_positional_index(preprocessor.tokens, filename)
        with open(saved_index, "wb") as f:
            pickle.dump(inverted_index, f)
        print("Created inverted index from scratch")

    print(f"Total tokens: {len(inverted_index.index)}")
    # with open("tokens", "w") as f:
    #     f.write(str(list(inverted_index.index.keys())))

    # Create the application
    app = QApplication(sys.argv)
    window = QWidget()

    # Input and output labels
    label = QLabel("Enter query:")
    input_text = QLineEdit()
    output_label = QLabel("Output:")

    # Create button and connect it to the function
    button = QPushButton("Submit", window)

    # Function to get query result on each button press
    def get_answer(query) -> str:
        posting = inverted_index.parse_query(query)
        if posting == None:
            return "NIL"
        else:
            return posting.result()

    enter_shortcut = QShortcut(QKeySequence(Qt.Key_Return), window)
    enter_shortcut.activated.connect(button.click)
    button.clicked.connect(
        lambda: output_label.setText(f"Output: {get_answer(input_text.text())}")
    )

    # Set up the layout
    layout = QVBoxLayout()
    layout.addWidget(label)
    layout.addWidget(input_text)
    layout.addWidget(button)
    layout.addWidget(output_label)

    # Set the layout for the main window
    window.setLayout(layout)

    # Set up the main window
    window.setWindowTitle("IR Boolean Model (21K-3298)")
    window.show()

    # Run the application
    sys.exit(app.exec_())

    # Proof of concept for command-line
    while True:
        query = input("Enter query: ")
        posting = inverted_index.parse_query(query)
        if posting == None:
            print("NIL")
        else:
            print(posting.result())
