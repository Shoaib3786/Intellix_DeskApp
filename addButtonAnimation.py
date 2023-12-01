import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSizePolicy

class MyProgram(QWidget):
    def __init__(self):
        super(MyProgram, self).__init__()

        self.init_ui()

    def init_ui(self):
        # Create a button
        self.my_button = QPushButton('Click Me!', self)
        self.my_button.clicked.connect(self.on_button_click)

        # Set the style sheet for the button
        self.my_button.setStyleSheet(
            "QPushButton {"
            "   background-color: black;"
            "   border: 2px solid white;"
            "   color: white;"
            "   border-radius: 7px;"
            "   width: 20%;" 
            "}"
            "QPushButton:hover {"
            "   background-color: white;"  # Change color on hover if needed
            "   color: black;"
            "}"
        )

        self.my_button.setFixedSize(150,30)


        # Create a layout and add the button to it
        layout = QVBoxLayout()
        layout.addWidget(self.my_button)

        # Set the layout for the main window
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('My PyQt5 Program')
        self.setGeometry(100, 100, 400, 300)

        # Set stretch factor to make the button responsive
        layout.setStretchFactor(self.my_button, 20)


    def on_button_click(self):
        print('Button Clicked!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyProgram()
    window.show()
    sys.exit(app.exec_())

