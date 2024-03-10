import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)

# Create the application
app = QApplication(sys.argv)

# Create the main window
window = QWidget()

# Create widgets
label = QLabel("Enter text:")
input_text = QLineEdit()
output_label = QLabel("Output:")

# Create button and connect it to the function
button = QPushButton("Submit", window)
button.clicked.connect(lambda: output_label.setText(f"Output: {input_text.text()}"))

# Set up the layout
layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(input_text)
layout.addWidget(button)
layout.addWidget(output_label)

# Set the layout for the main window
window.setLayout(layout)

# Set up the main window
window.setWindowTitle("Simple PyQt5 App")
window.show()

# Run the application
sys.exit(app.exec_())
