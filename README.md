# ⚖️ LegalEase-AI Law Assistant

LegalEase-AI is an intelligent, user-friendly law assistant that helps simplify complex legal documents, answer legal questions using Agentic AI, and estimate lawyer consultation costs — all tailored for Indian law.

---

## 🚀 Features

### 📝 1. Legal Document Summarizer
- Upload legal documents (PDFs)
- Get simplified, easy-to-understand summaries
- Powered by NLP and legal data from Indian law

### 💬 2. Agentic AI Chatbot
- Ask legal questions in plain English or Tamil
- Smartly responds using real legal data stored in PostgreSQL
- Ideal for quick legal guidance, not a substitute for a real lawyer

### 📊 3. Consultation Cost Estimator
- Predicts legal consultation costs based on:
  - Type of case
  - Location
  - Case complexity
- Data-driven using real-world lawyer consultation datasets

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, Bootstrap
- **Backend**: Python (Flask)
- **Database**: PostgreSQL
- **AI & NLP**: OpenAI API, Agentic AI logic
- **Environment**: `.env` file with `python-dotenv`

---

## 📂 Folder Structure

```

LegalEase-AI-law-assistant/
│
├── templates/             # HTML templates (summarizer, chatbot, estimator)
├── static/                # CSS, JS, and assets
├── app.py                 # Flask backend logic
├── summarizer.py          # Summarization logic
├── chatbot\_agent.py       # Agentic chatbot logic
├── cost\_estimator.py      # Consultation cost estimator
├── database/              # PostgreSQL schema & sample data
├── .env                   # API keys (not pushed to GitHub)
└── README.md              # Project overview

````

---

## 🧑‍💻 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/dhivya776/LegalEase-AI-law-assistant.git
   cd LegalEase-AI-law-assistant
````

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   Create a `.env` file:

   ```
   OPENAI_API_KEY=your-api-key
   ```

4. **Run the app**

   ```bash
   python app.py
   ```

---

## 🧠 How It Works

* **Summarizer**: Uses NLP and custom rules to extract and rephrase key points from legal docs
* **Chatbot**: Uses Agentic AI patterns to look up legal info and respond contextually
* **Cost Estimator**: Fetches data from PostgreSQL and applies statistical logic to provide fair estimates

---

## 🧾 Legal Notice

This tool provides **informational support only**. It is **not a substitute** for professional legal advice. Always consult a licensed lawyer for serious matters.

---

## 💡 Future Enhancements

* 🧾 Multi-language support (Hindi, Tamil)
* 📲 Mobile responsive design
* 📁 Upload multiple files
* 🧠 Custom-trained LLM for Indian Law

---

## 🙋‍♀️ Author

**Dhivya**
Front-end developer & ML enthusiast
📧 [LinkedIn](https://www.linkedin.com/in/dhivya776)

---

## ⭐ Star this repo

If you found this helpful, don’t forget to star ⭐ the repository!

```

---
