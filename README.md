# TruthLens — Fake News Detection System

AI-powered web app that detects fake news using machine learning and NLP.
Built with **Python · Streamlit · MySQL · scikit-learn**.

---

## Project Structure

```
truthlens/
├── app.py                  # Main Streamlit entry point
├── setup.py                # One-time DB init + admin account creator
├── requirements.txt
├── .env.example            # Copy to .env and fill credentials
├── fake_news_dataset.csv   # ← Place your dataset here (project root)
│
├── ml/
│   ├── train_model.py      # Train the ML model (run once)
│   ├── predictor.py        # Load model & run predictions
│   └── model.pkl           # Generated after training (git-ignored)
│
├── pages/
│   ├── home.py             # Landing page with live stats
│   ├── analyze.py          # Core: paste/upload & analyze news
│   ├── community.py        # Public review: vote + discuss
│   ├── history.py          # Per-user analysis history
│   ├── admin.py            # Admin: manage users & analyses
│   ├── login.py
│   └── register.py
│
└── utils/
    ├── db.py               # MySQL connection + schema creation
    ├── auth.py             # Password hashing, login, register
    └── analysis_db.py      # CRUD for analyses, votes, comments
```

---

## Quick Start

### 1. Prerequisites
- Python 3.10+
- MySQL 8.0+ running locally
- VS Code (recommended)

### 2. Clone / open the project in VS Code
```bash
cd truthlens
```

### 3. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure your database credentials
```bash
# Copy the example env file
cp .env.example .env
```
Open `.env` and set your MySQL credentials:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=truthlens_db
```

### 6. Place the dataset
Copy `fake_news_dataset.csv` into the **project root** (same folder as `app.py`).
The file must contain columns: `title`, `text`, `label` (1 = fake, 0 = real).

### 7. Initialize the database
```bash
python setup.py
```
This creates the `truthlens_db` database, all tables, and a default admin account:
- **Username:** `admin`
- **Password:** `admin123`  ⚠️ Change this after first login!

### 8. Train the ML model
```bash
python ml/train_model.py
```
This reads the dataset, trains a Logistic Regression + TF-IDF pipeline,
prints accuracy, and saves `ml/model.pkl`.
Training takes ~1–2 minutes for 72K rows.

### 9. Run the app
```bash
streamlit run app.py
```
Open your browser at **http://localhost:8501**

---

## Database Schema

| Table       | Key Columns                                                        |
|-------------|---------------------------------------------------------------------|
| `users`     | id, username, email, password (SHA-256), role, created_at          |
| `analyses`  | id, user_id, title, text_snippet, full_text, prediction, confidence, is_public |
| `votes`     | id, analysis_id, user_id, vote (up/down)                           |
| `comments`  | id, analysis_id, user_id, content, created_at                      |

---

## Features

| Feature                     | Description                                              |
|-----------------------------|----------------------------------------------------------|
| **User Auth**               | Register / Login with hashed passwords                   |
| **Paste or Upload**         | Analyze by pasting text or uploading a `.txt` file       |
| **ML Prediction**           | Logistic Regression + TF-IDF, ~95%+ accuracy            |
| **Confidence Score**        | Fake/Real probability displayed with progress bar        |
| **Save History**            | Every analysis saved to MySQL per user                   |
| **Publish for Review**      | Fake news can be optionally shared publicly              |
| **Community Voting**        | Upvote / Downvote the AI verdict                         |
| **Discussion Threads**      | Comment on public posts (anonymized)                     |
| **Admin Dashboard**         | Manage users, view all analyses, delete content          |

---

## VS Code Tips

- Install the **Python** and **Pylance** extensions.
- Set the interpreter to your venv: `Ctrl+Shift+P` → *Python: Select Interpreter* → choose `venv`.
- Use the integrated terminal to run `streamlit run app.py`.

---

## Tech Stack

| Layer       | Technology                     |
|-------------|--------------------------------|
| Frontend    | Streamlit 1.35+                |
| Backend     | Python 3.10+                   |
| ML          | scikit-learn (LR + TF-IDF)     |
| Database    | MySQL 8.0 via mysql-connector  |
| Auth        | SHA-256 password hashing       |
