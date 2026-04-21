

from utils.db import init_db
from utils.auth import register_user


def main():
    print("=== TruthLens Setup ===\n")

    print("Step 1: Initializing database …")
    init_db()
    print("   Database and tables created.\n")

    print("Step 2: Creating default admin account …")
    ok, msg = register_user(
        username="admin",
        email="admin@truthlens.local",
        password="admin123",
        role="admin",
    )
    if ok:
        print("  Admin account created.")
        print("     Username : admin")
        print("     Password : admin123")
        print("  Change this password immediately after first login!\n")
    else:
        if "Duplicate" in msg or "already exists" in msg.lower():
            print("   Admin account already exists — skipping.\n")
        else:
            print(f"   Could not create admin: {msg}\n")

    print("Setup complete! Run the app with:\n")
    print("    streamlit run app.py\n")


if __name__ == "__main__":
    main()
