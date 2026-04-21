# Contributing to TruthLens

Welcome to the TruthLens project! This guide explains how to set up the project locally and collaborate with the team using Git and GitHub.

---

## Team Setup (Do This Once)

### 1. Accept the GitHub Invitation
Check your email for a collaboration invite from GitHub and accept it.

### 2. Clone the Repository
```bash
git clone https://github.com/Har-leen/truthlens.git
cd truthlens
```

### 3. Create a Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Set Up Your `.env` File
```bash
copy .env.example .env
```
Open `.env` and fill in **your own** MySQL credentials:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_own_mysql_password
DB_NAME=truthlens_db
```

### 6. Get the Dataset
Ask a team member to share `fake_news_dataset.csv` via WhatsApp or Google Drive.
Place it in the **project root** (same folder as `app.py`).

### 7. Initialize Your Local Database
```bash
python setup.py
```

### 8. Train the ML Model
```bash
python ml/train_model.py
```

### 9. Run the App
```bash
streamlit run app.py
```

---

## Daily Git Workflow

### Before starting work — always pull latest changes first:
```bash
git pull origin main
```

### After making changes — push your work:
```bash
git add .
git commit -m "Brief description of what you changed"
git push origin main
```

---

## Branch Workflow (Recommended)

Instead of everyone pushing directly to `main`, create your own branch:

```bash
# Create and switch to your branch
git checkout -b your-name/feature-name

# Example
git checkout -b harleen/login-page
```

Push your branch:
```bash
git push origin your-name/feature-name
```

Then open a **Pull Request** on GitHub so the team can review before merging to `main`.

---

## Important Rules

- **Never commit your `.env` file** — it contains your password and is git-ignored
- **Never commit `ml/model.pkl`** — it's large and git-ignored, each member trains locally
- **Never commit `fake_news_dataset.csv`** — share via Google Drive/WhatsApp instead
- Always `git pull` before starting work to avoid conflicts

---

## Project Structure

```
truthlens/
├── app.py              # Main entry point
├── setup.py            # DB initializer (run once)
├── requirements.txt    # Python dependencies
├── .env.example        # Copy to .env and fill credentials
├── ml/
│   ├── train_model.py  # Train the ML model (run once)
│   └── predictor.py    # Prediction logic
├── views/              # All Streamlit pages
│   ├── home.py
│   ├── analyze.py
│   ├── community.py
│   ├── history.py
│   ├── admin.py
│   ├── login.py
│   └── register.py
└── utils/
    ├── db.py           # Database connection
    ├── auth.py         # Login / Register logic
    └── analysis_db.py  # Analysis, votes, comments
```

---

## Need Help?

Contact the project owner on GitHub: [@Har-leen](https://github.com/Har-leen)
