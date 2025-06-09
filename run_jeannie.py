
# Starterversion - My Dream of Jeannie
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt

class JeannieWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My Dream of Jeannie')
        self.setGeometry(100, 100, 400, 500)

        layout = QVBoxLayout()

        # Smoke Animation
        self.smoke_label = QLabel(self)
        self.movie = QMovie('jeannie/animations/smoke.gif')
        self.smoke_label.setMovie(self.movie)
        self.movie.start()
        layout.addWidget(self.smoke_label)

        # Chat Display
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # Input Field
        self.input_field = QTextEdit(self)
        self.input_field.setFixedHeight(50)
        layout.addWidget(self.input_field)

        # Send Button
        send_button = QPushButton('Send', self)
        send_button.clicked.connect(self.handle_send)
        layout.addWidget(send_button)

        self.setLayout(layout)

        # Initial Greeting
        self.chat_display.append("Jeannie: Hallo, Meister! Was kann ich für dich tun?")

    def handle_send(self):
        user_text = self.input_field.toPlainText().strip()
        if user_text:
            self.chat_display.append(f"Du: {user_text}")
            self.chat_display.append("Jeannie: Ich arbeite noch an meinen Antworten ;)")
            self.input_field.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = JeannieWindow()
    window.show()
    sys.exit(app.exec_())
