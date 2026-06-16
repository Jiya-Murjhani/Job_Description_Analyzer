# 🎯 Job Description Analyzer

<div align="center">

**An AI-powered resume analysis tool that tells you exactly how well you match a job — and precisely how to close every gap.**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=for-the-badge)](https://groq.com)

[Live Demo](https://jobdescriptionanalyzer-cqdrzjpgqqgcjvzrd9n8ww.streamlit.app/) · [Report Bug](https://github.com/Jiya-Murjhani/Job_Description_Analyzer/issues) · [Request Feature](https://github.com/Jiya-Murjhani/Job_Description_Analyzer/issues)

</div>

---

## 📌 The Problem This Solves

Most job seekers apply blindly — paste resume, click submit, wonder why they hear nothing back.

The real reason is almost always the same: **their resume doesn't speak the language of that specific job description.** Keywords are missing, relevant skills are buried, and they have no idea what the gap actually is.

This app solves that. **Precisely. Instantly. For any role.**

---

## ✨ What It Does

Upload your resume PDF and paste any job description. In seconds you get:

| Output | Description |
|--------|-------------|
| 📊 **Match Score** | Percentage match with visual progress bar |
| 🎯 **Required Skills** | Top skills the JD is actually asking for |
| ✅ **Skills You Have** | Green — Strong match or Partial match with confidence level |
| ❌ **Skills You're Missing** | Red — Exact gaps between your resume and the JD |
| 💡 **How to Fix Each Gap** | Specific suggestion: rewrite a bullet OR build a project |
| 🧠 **Expert Recommendation** | One high-impact, personalized action to improve your chances |



## 🧠 How the AI Analysis Works

This isn't simple keyword matching. The app uses **LLaMA 3.3 70B via Groq API** with a carefully engineered prompt that:

- Extracts only **real technical skills** from the JD — no soft skills, no attitude statements
- Detects **seniority level** of the role and calibrates accordingly (internship vs mid-level vs senior)
- Assigns **confidence levels** per skill — Strong Match vs Partial Match
- Counts **certifications and coursework** as valid evidence for entry-level roles
- Applies **deduplication logic** — "Python" and "Knowledge of Python fundamentals" count as one
- Calculates score as: `(strong matches × 1) + (partial matches × 0.5) / total skills × 100`
- Generates **anti-hallucination suggestions** — only references what's actually in your resume

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| UI | Streamlit | Interface, file upload, progress bar, visual output |
| AI Brain | Groq API — LLaMA 3.3 70B | Resume vs JD analysis, structured JSON output |
| PDF Parsing | PyPDF2 | Extract clean text from uploaded resume PDF |
| Config | python-dotenv | Secure API key management |
| Language | Python 3.9+ | Core application logic |

---

## 📁 Project Structure

```
job-description-analyzer/
│
├── app.py                          # Main Streamlit application
│
├── utils/
│   ├── Groq_connection.py          # Groq API integration + prompt engineering
│   └── pdf_parser.py               # PDF text extraction logic
│
├── requirements.txt                # Project dependencies
├── .env                            # API keys (not committed to Git)
├── .gitignore                      # Ignores .env and cache files
└── README.md                       # You are here
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- A free Groq API key → [Get one here](https://console.groq.com)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/Jiya-Murjhani/job-description-analyzer.git
cd job-description-analyzer
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up your API key**

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

**4. Run the app**
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 📦 Requirements

```
streamlit
groq
PyPDF2
python-dotenv
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 💡 Key Technical Concepts Demonstrated

**Structured JSON output from LLM**
Instead of asking the model to return plain text, the prompt engineers a strict JSON schema that Python then parses and renders dynamically. This is the pattern behind production document intelligence systems.

**PDF parsing with PyPDF2**
Handles multi-page resume PDFs, extracts clean text page by page with blank-page safety checks.

**Two-input coordination**
Simultaneously handles a file upload (PDF) and a text input (JD) before making a single API call — coordinating multiple input types is a real-world AI engineering pattern.

**Prompt engineering for accuracy**
13 strict rules in the system prompt handle edge cases: soft skill exclusion, deduplication, seniority detection, confidence levels, anti-hallucination constraints, and coursework/certification counting.

**Dynamic UI rendering**
Green success blocks, yellow warning blocks, red error blocks, and expanders rendered based on live API data — not hardcoded content.

---

## 🔍 Example Output

```
Match Score: 75%
6 strong matches, 3 partial matches out of 10 required skills

✅ Python                  — Strong Match
✅ Machine Learning        — Strong Match
✅ Pandas                  — Strong Match
✅ NumPy                   — Strong Match
✅ Predictive Analytics    — Strong Match
✅ Data Analysis           — Strong Match
🟡 Scikit-learn            — Partial Match
🟡 Data Visualization      — Partial Match
🟡 Statistics              — Partial Match

❌ Missing Skills:
✗ SQL
✗ Deep Learning

💡 How to Fix Each Gap:

SQL:
Project: Build a Python project that connects to a MySQL database,
runs analytical queries on a sales dataset, and exports insights
to a CSV report — push it to GitHub with clear documentation.

Deep Learning:
Project: Train a simple neural network using TensorFlow/Keras
on the MNIST dataset, document the architecture, training accuracy,
and loss curves, and publish the notebook on GitHub.

🧠 Expert Recommendation:
"Add one Scikit-learn project to your GitHub that covers model
training, evaluation metrics, and a confusion matrix — it directly
closes the most visible technical gap for this role."
```

---

## ⚙️ How to Use

1. Open the app in your browser
2. Upload your resume as a **PDF file**
3. Paste any job description into the text area
4. Click **Analyze**
5. Review your match score, skill gaps, and suggestions
6. Use the suggestions to update your resume or build targeted projects

---

## 🛡️ Edge Cases Handled

- Empty or unreadable PDF → clear error message
- Job description too short → warning shown before analysis
- API failure → graceful error with retry prompt
- Markdown fences in API response → auto-stripped before JSON parsing
- Missing JSON fields → `result.get()` with safe fallbacks

---

## 🗺️ Roadmap

- [ ] Support for DOCX resume uploads
- [ ] Side-by-side comparison of multiple JDs
- [ ] Resume rewrite suggestions as downloadable output
- [ ] History — save and compare past analyses
- [ ] Chrome extension for one-click JD analysis from any job board

---

## 👩‍💻 Author

**Jiya Murjhani**

BCA Graduate — MediCaps University, Indore | CGPA: 8.58

AI/ML & Python Developer | Open to Remote Opportunities

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/jiya-murjhani)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/Jiya-Murjhani)
[![Email](https://img.shields.io/badge/Email-D14836?style=flat&logo=gmail&logoColor=white)](mailto:jiya.murjhani@gmail.com)

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) — for blazing fast LLaMA inference
- [Streamlit](https://streamlit.io) — for making Python UI this simple

---

<div align="center">

**If this project helped you, consider giving it a ⭐ on GitHub**

*Built with Python, Groq API, and a lot of prompt engineering.*

</div>