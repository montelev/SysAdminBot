# SysAdminBot 🖥️
**AI-Powered Infrastructure Scripting Tool**

SysAdminBot is a web-based automation tool that bridges the gap between plain English and complex infrastructure management. Type a task, choose your environment, and receive a secure, production-ready PowerShell or Bash script — complete with inline comments and error handling.

**Live Demo:** *(deploy to Streamlit Community Cloud and paste URL here)*

---

## Features

- 🪟 **Windows Server / PowerShell** — Active Directory, IIS, Group Policy, Hyper-V tasks
- 🐧 **Linux / Bash** — systemd, cron, OpenSSH, user & group management
- 🔒 **Security-first output** — every script enforces least privilege, secure credential objects, and try/catch error handling
- 💬 **Inline comments** — every non-trivial line is explained for review and auditing
- ⬇️ **One-click download** — save the script as `.ps1` or `.sh` directly from the browser

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend & Backend | [Streamlit](https://streamlit.io) (Python) |
| AI Engine | [Google Gemini API](https://aistudio.google.com) (`gemini-1.5-flash`) |
| Deployment | Streamlit Community Cloud |

---

## Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/SysAdminBot.git
cd SysAdminBot
```

### 2. Create a virtual environment & install dependencies
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Add your Gemini API key
```bash
cp .env.example .env
# Edit .env and replace the placeholder with your real key
# Get a free key at: https://aistudio.google.com/app/apikey
```

### 4. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Deploying to Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app** → select `app.py`.
3. Under **Advanced settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your_actual_key_here"
   ```
4. Click **Deploy**. Your live URL is ready to share.

---

## Project Structure

```
SysAdminBot/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example        # API key template (safe to commit)
└── README.md
```

---

## Resume Entry

> **SysAdminBot: AI-Powered Infrastructure Scripting Tool** | June 2026
> - Developed a responsive web application using Python and Streamlit to automate repetitive System Administration and Identity Management tasks.
> - Integrated the Google Gemini API to parse unstructured text inputs and translate them into secure, production-grade PowerShell and Bash scripts.
> - Optimized system prompt engineering to enforce enterprise security best practices, including inline error handling and secure variable definition.
> - Managed codebase utilizing Git/GitHub and deployed the functional application to a cloud environment for live stakeholder demonstration.

---

*Built with Python, Streamlit, and Google Gemini.*
