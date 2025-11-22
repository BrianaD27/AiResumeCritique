# AI Resume Criticizer 📝

AI Resume Criticizer is a Streamlit-powered web application that analyzes your resume using OpenAI's latest models and provides tailored, structured feedback. Whether you have a dream job in mind or need help discovering suitable roles, this app gives you AI-generated insights to improve your resume and apply confidently.

The app supports the following resume formats:

- **PDF** (`.pdf`)
- **Text** (`.txt`)
- **Word Documents** (`.docx`)
- **Markdown** (`.md`)

---

## 🚀 Features

- Personalized resume analysis (content clarity, quantified impact, skill strength, etc.)
- Bullet-point preservation in `.docx` resumes
- Optional dream job input for targeted recommendations
- Automatic suggestion of roles if no role is provided
- Company recommendations based on your resume
- Animated "Analysis Loading…" UX while AI processes your file
- Clean, modern UI built with Streamlit

---

## 🔧 Requirements

Before running the project, make sure you have:

- **Python 3.10+**
- **uv** (fast Python package manager)  
  Install uv here: https://github.com/astral-sh/uv
- An **OpenAI API Key**  
  Get one at: https://platform.openai.com

---

## 🗂 Project Structure

Your project should look like this:

```
AiResumeCritiquer/
├── .streamlit/
│   └── config.toml
├── .venv/                # created automatically by uv (optional)
├── .env                  # you will create this
├── .python-version
├── main.py               # Streamlit application
├── pyproject.toml        # uv-managed dependencies
├── README.md
└── uv.lock
```

---

## 📥 Installation & Setup

Follow these steps to download, configure, and run the application.

---

### 1️⃣ Clone or Download the Repository

```bash
git clone https://github.com/<your-username>/AiResumeCritiquer.git
cd AiResumeCritiquer
```

Or download the ZIP and extract it.

### 2️⃣ Install Dependencies using uv

This project uses uv instead of pip.

Install all dependencies with:

```bash
uv sync
```

If any package is missing, you can add it manually:

```bash
uv add streamlit openai python-dotenv pypdf2 python-docx
```

### 3️⃣ Add Your OpenAI API Key

Create a `.env` file in the root of the project:

```bash
AiResumeCritiquer/.env
```

Add your key:

```env
OPEN_API_KEY=sk-your-openai-key-here
```

⚠️ Do NOT commit this file to GitHub.

### 4️⃣ Run the Application

Use uv to run Streamlit with the project environment:

```bash
uv run streamlit run main.py
```

Then open the local URL that Streamlit prints, usually:

```
http://localhost:8501
```

---

## 🖥️ How to Use the App

1. Open the app in your browser.
2. Upload your resume in PDF, TXT, DOCX, or MD format.
3. (Optional) Enter your dream job or role.
4. Click **Analyze Resume**.
5. Watch the animated "Your Analysis is Loading…" message.
6. Receive detailed AI-powered feedback, including:
   - Strengths and weaknesses
   - Skill and experience assessments
   - Suggested job roles (if none provided)
   - Companies that match your background
   - Specific improvements to enhance your resume

---

## 🧠 How It Works

- **PyPDF2** extracts text from PDFs
- **python-docx** extracts text from DOCX (including bullet points!)
- Markdown and text files are read directly
- The extracted content is sent to OpenAI's **gpt-4.1-mini** model
- Streamlit handles UI, layout, and interactive elements
- Custom CSS provides loading animations and styling

---

## 🐛 Troubleshooting

### ❌ OPEN_API_KEY is missing

Create an `.env` file and add:

```env
OPEN_API_KEY=sk-your-key
```

Make sure you're running the app from the project root.

### ❌ PDF text comes out blank

Some PDFs are images, not text. Try:

- Exporting the PDF as `.docx`
- Copy/pasting into a `.txt` file
- Using OCR before uploading

### ❌ Missing packages

Run:

```bash
uv sync
```

Or if needed:

```bash
uv add <package-name>
```

---

## 🎨 Customization

You can modify:

- **The theme** → `.streamlit/config.toml`
- **The prompts** → inside `main.py`
- **The AI model** → change `model='gpt-4.1-mini'`
- **File upload types** → update `type=[...]` in the uploader
- **Loading animations** → edit the CSS block in `main.py`

---

## 🌟 Enjoy Your AI Resume Criticizer!

Happy building — and may your resumes shine ✨🚀
