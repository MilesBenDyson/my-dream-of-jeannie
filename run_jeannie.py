# Starterversion - My Dream of Jeannie
import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTextEdit, QPushButton, QDesktopWidget
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtCore import Qt, QTimer

# --- SPLASH WINDOW ---
class SplashWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My Dream of Jeannie - Lade Rauch...')
        self.setGeometry(100, 100, 500, 500)

        layout = QVBoxLayout()

        self.smoke_label = QLabel(self)
        self.smoke_label.setFixedSize(800, 800)
        self.movie = QMovie('jeannie/animations/smoke.gif')
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setScaledSize(self.smoke_label.size())
        self.smoke_label.setMovie(self.movie)
        self.movie.start()

        layout.addWidget(self.smoke_label)
        self.setLayout(layout)

        # Fenster zentrieren
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Nach 1 Sekunde automatisch auf Hauptfenster wechseln
        QTimer.singleShot(1000, self.transition_to_main)

    def transition_to_main(self):
        self.movie.stop()
        self.close()
        self.main_window = JeannieWindow()
        self.main_window.show()


# --- JEANNIE MAIN WINDOW ---
class JeannieWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowOpacity(0.0)  # Start unsichtbar
        QTimer.singleShot(100, self.fade_in)

        layout = QVBoxLayout()

        # Fenster zentrieren
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Avatar
        self.avatar_label = QLabel(self)
        pixmap = QPixmap('jeannie/jeannie_avatar.png')
        pixmap = pixmap.scaledToWidth(200, Qt.SmoothTransformation)
        self.avatar_label.setPixmap(pixmap)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.avatar_label)

        # Sprechblase (Antwort-Label)
        self.speech_label = QLabel("Jeannie: Hallo, Meister!", self)
        self.speech_label.setAlignment(Qt.AlignCenter)
        self.speech_label.setStyleSheet("""
            background-color: #ffffff;
            border: 2px solid #ff69b4;
            border-radius: 10px;
            padding: 10px;
            font-family: 'Courier New';
            font-size: 14px;
            color: #000000;
        """)
        layout.addWidget(self.speech_label)


        # Input Field (80er Style)
        self.input_field = QTextEdit(self)
        self.input_field.setFixedHeight(50)
        self.input_field.setStyleSheet("""
            background-color: #222222;
            color: #39ff14;
            font-family: 'Courier New';
            font-size: 14px;
        """)
        layout.addWidget(self.input_field)

        # Send Button
        send_button = QPushButton('Send', self)
        send_button.clicked.connect(self.handle_send)
        layout.addWidget(send_button)

        self.setLayout(layout)

        # Initial Greeting
        self.speech_label.setText("Jeannie: Hallo, Meister! Was kann ich für dich tun?")


    def handle_send(self):
        user_text = self.input_field.toPlainText().strip()
        if user_text:


            antworten = [
                "Ich bin ganz Ohr, Meister.",
                "Ich schau mal in meine Kristallkugel...",
                "Hmmm... das muss ich noch lernen.",
                "Könntest du das bitte anders formulieren?",
                "Wie interessant, Meister!"
            ]

            self.speech_label.setText(f"Jeannie: {random.choice(antworten)}")
            self.input_field.clear()

    def fade_in(self):
        for i in range(0, 11):
            QTimer.singleShot(i * 50, lambda opacity=i: self.setWindowOpacity(opacity / 10))


# --- MAIN ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = SplashWindow()
    splash.show()
    sys.exit(app.exec_())
