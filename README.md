# 🧞 My Dream of Jeannie - Virtual AI Assistant

**Locally running, personalized virtual assistant with personality**  
_"She appears in a cloud of pink smoke and serves her master."_  

---

## ✨ Features

- Local AI assistant (offline-capable)
- Personalized greetings
- Contextual memory (via FAISS or similar)
- GUI with appear/disappear animation (Jeannie cloud)
- Interactive chatbot with personality
- Custom command interface (file search, local actions, music control, etc.)
- Role-playing capabilities (can act "cheeky" if allowed 😉)

---

## 🚀 Current Status

- Basic prototype running (Python GUI + local LLM)
- Memory / Knowledge Base in progress
- Appearance & animations: TODO
- Command framework: Beta

---

## 🛠 Stack / Used Technologies

- Python 3.x
- PyQt / PySide (GUI)
- FAISS / Local DB for memory
- Local LLMs (GPT4All / Mistral / Ollama)
- TTS / STT (optional)
- Custom animations (GIF / Canvas)

---

## 💡 Installation

```bash
git clone https://github.com/MilesBenDyson/my-dream-of-jeannie.git
cd my-dream-of-jeannie
# Setup virtualenv, install requirements
pip install -r requirements.txt
python run_jeannie.py
