# Enigma - Study Tool (WinHacks 2025)

Enigma is an AI-powered study tool designed to help students summarize notes, generate flashcards, extract text from PDFs, and enhance learning efficiency. Built using **Flask (backend) and React (frontend)**, it integrates **AI-driven summarization, OCR, and Q&A features**.

## 🚀 Features
- 📚 **AI Summarization** - Upload notes or PDFs, and get concise summaries.
- 📝 **PDF Text Extraction** - Extract readable text from PDF documents.
- 🎯 **Flashcard Generator** - Automatically create flashcards from study materials.
- 🎙️ **Voice-to-Text** - Convert spoken words into text notes.
- ✍️ **Handwritten Notes OCR** - Scan and digitize handwritten notes.
- ⏳ **Study Timer** - Track study sessions and breaks using Pomodoro technique.
- 🤖 **AI Chatbot for Q&A** - Ask AI questions based on your study material.

## 🛠️ Tech Stack
### **Backend:**
- **Flask** - Web framework for Python.
- **PyMuPDF** - Extract text from PDFs.
- **Tesseract OCR** - Process handwritten notes.
- **Google Speech-to-Text API** - Convert voice to text.
- **Hugging Face Transformers** - AI-powered text summarization and Q&A.

### **Frontend:**
- **React** - User-friendly interface.
- **Axios** - Handle API requests.
- **CSS** - For styling.

## 🖥️ Installation & Setup
### 1️⃣ **Clone the Repository**
```sh
 git clone https://github.com/YOUR-USERNAME/Enigma.git
 cd Enigma
```

### 2️⃣ **Backend Setup (Flask)**
```sh
 cd backend
 python -m venv venv  # Create a virtual environment
 source venv/bin/activate  # (Windows: venv\Scripts\activate)
 pip install -r requirements.txt
```

### 3️⃣ **Set Up Environment Variables**
Create a `.env` file in the **backend** folder and add:
```sh
HUGGING_FACE_API_KEY=your_api_key_here
```

### 4️⃣ **Run Flask Server**
```sh
 python app.py
```

### 5️⃣ **Frontend Setup (React)**
```sh
 cd frontend
 npm install
 npm start
```

## 📌 How to Use
1. **Upload a PDF** or **Paste Text** for summarization.
2. Click **"Summarize"** to generate AI-powered summaries.
3. Generate **Flashcards** to test yourself.
4. Record **Voice Notes** and convert them into text.
5. Scan **Handwritten Notes** and extract text.
6. Track your study sessions with the **Study Timer**.

## 🤝 Contribution Guidelines
- **Fork the repository & clone it locally.**
- Create a **new branch** for your feature/fix.
- Commit changes & push to your branch.
- Submit a **pull request**.

## 📜 License
This project is **open-source** under the [MIT License](LICENSE).

## 👨‍💻 Team
- **Your Name** - Backend Developer
- **Other Team Members** - Role (Frontend, Design, AI, etc.)

### 🌟 *WinHacks 2025 Submission*

