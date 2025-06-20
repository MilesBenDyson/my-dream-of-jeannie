# My Dream of Jeannie – Kristallkugel-Version
import sys
import random
import urllib.request
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTextEdit, QPushButton, QDesktopWidget
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtCore import Qt, QTimer
from gpt4all import GPT4All
import requests
from bs4 import BeautifulSoup

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

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

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
        self.kristall_status = False
        self.model = None
        self.model_path = r"C:\\Users\\bensc\\Desktop\\IT\\KI_models\\em_german_mistral_v01.Q4_K_M.gguf"
        self.initUI()

    def scrape_urls_from_file(self, prompt, filepath="webseiten.txt"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                urls = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return "Die Liste mit Webseiten konnte nicht gefunden werden, Meister."

        alle_texte = ""
        for url in urls:
            try:
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.text, "html.parser")
                texte = soup.get_text(separator=" ", strip=True)
                alle_texte += f"\n--- Inhalt von: {url} ---\n{texte[:1000]}...\n"
            except Exception as e:
                alle_texte += f"\n--- Fehler bei {url}: {e} ---\n"

        frage = f"""Ich habe folgende Webseiten gelesen:\n{alle_texte}\n\nBitte beantworte auf Basis dieser Informationen die folgende Frage:\n{prompt}"""
        return self.ask_local_model(frage)

    def wiki_suche(self, suchbegriff):
        thema = suchbegriff.strip().replace("wiki:", "").strip()
        url = f"https://de.wikipedia.org/wiki/{thema.replace(' ', '_')}"
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            artikel_text = soup.get_text(separator=" ", strip=True)
            frage = f"Ich habe den Wikipedia-Artikel über '{thema}' gelesen. Hier ist der Textauszug:\n{artikel_text[:1500]}...\n\nWas kannst du mir dazu sagen?"
            return self.ask_local_model(frage)
        except Exception as e:
            return f"Jeannie: Ich konnte den Wikipedia-Artikel leider nicht laden, Meister. ({e})"

    def initUI(self):
        self.setWindowOpacity(0.0)
        QTimer.singleShot(100, self.fade_in)

        layout = QVBoxLayout()

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.avatar_label = QLabel(self)
        pixmap = QPixmap('jeannie/jeannie_avatar.png').scaledToWidth(200, Qt.SmoothTransformation)
        self.avatar_label.setPixmap(pixmap)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.avatar_label)

        self.kugel_label = QLabel(self)
        self.kugel_pixmap_off = QPixmap('jeannie/kugel_off.png').scaledToWidth(100, Qt.SmoothTransformation)
        self.kugel_pixmap_on = QPixmap('jeannie/kugel_on.png').scaledToWidth(100, Qt.SmoothTransformation)
        self.kugel_label.setPixmap(self.kugel_pixmap_off)
        self.kugel_label.setAlignment(Qt.AlignCenter)
        self.kugel_label.mousePressEvent = self.toggle_kristall
        layout.addWidget(self.kugel_label)

        from PyQt5.QtWidgets import QScrollArea

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedHeight(150)

        self.speech_label = QLabel("Jeannie: Hallo, Meister!")
        self.speech_label.setAlignment(Qt.AlignTop)
        self.speech_label.setWordWrap(True)
        self.speech_label.setStyleSheet("""
            background-color: #ffffff;
            border: 2px solid #ff69b4;
            border-radius: 10px;
            padding: 10px;
            font-family: 'Courier New';
            font-size: 14px;
            color: #000000;
        """)

        self.scroll_area.setWidget(self.speech_label)
        layout.addWidget(self.scroll_area)

        self.input_field = QTextEdit(self)
        self.input_field.setFixedHeight(50)
        self.input_field.setStyleSheet("""
            background-color: #222222;
            color: #39ff14;
            font-family: 'Courier New';
            font-size: 14px;
        """)
        layout.addWidget(self.input_field)

        send_button = QPushButton('Send', self)
        send_button.clicked.connect(self.handle_send)
        layout.addWidget(send_button)

        self.setLayout(layout)

        self.speech_label.setText("Jeannie: Hallo, Meister! Was kann ich für dich tun?")
        print("🧠 Jeannie ist bereit. Lokales Modell wird beim ersten Bedarf geladen.")

    def toggle_kristall(self, event):
        if self.kristall_status:
            self.kristall_status = False
            self.kugel_label.setPixmap(self.kugel_pixmap_off)
            self.speech_label.setText("Jeannie: Ich ziehe mich zurück, Meister. Die Verbindung zum Universum ist getrennt.")
        else:
            if self.check_internet():
                self.kristall_status = True
                self.kugel_label.setPixmap(self.kugel_pixmap_on)
                self.speech_label.setText("Jeannie: Die Kristallkugel leuchtet, Meister. Ich bin mit dem Universum verbunden.")
            else:
                self.kristall_status = False
                self.kugel_label.setPixmap(self.kugel_pixmap_off)
                self.speech_label.setText("Jeannie: Oh nein Meister, die Kristallkugel kann gerade keine Verbindung mit dem Universum herstellen.")

    def check_internet(self):
        try:
            urllib.request.urlopen('http://google.com', timeout=2)
            return True
        except:
            return False

    def ask_local_model(self, prompt):
        if self.model is None:
            print("⏳ Lade lokales Modell...")
            self.model = GPT4All(model_name=self.model_path, model_path=self.model_path, allow_download=False)
        with self.model.chat_session():
            return self.model.generate(prompt)

    def handle_send(self):
        user_text = self.input_field.toPlainText().strip()
        if not user_text:
            return

        if user_text.lower().startswith("recherchiere:"):
            frage = user_text.replace("recherchiere:", "").strip()
            antwort = self.scrape_urls_from_file(frage)
            self.speech_label.setText(f"Jeannie: {antwort}")
            self.input_field.clear()
            return

        if user_text.lower().startswith("wiki:"):
            antwort = self.wiki_suche(user_text)
            self.speech_label.setText(f"Jeannie: {antwort}")
            self.input_field.clear()
            return

        antwort = self.ask_local_model(user_text)
        self.speech_label.setText(f"Jeannie: {antwort}")
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
