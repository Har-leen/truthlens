import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "truthlens_db"),
    "port":     int(os.getenv("DB_PORT", "3306")),
}


def get_connection():
    """Return a new MySQL connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        raise ConnectionError(f"MySQL connection failed: {e}")


def init_db():
    """Create all tables if they don't exist."""
    # First connect without a specific database to create it if needed
    try:
        temp_cfg = {k: v for k, v in DB_CONFIG.items() if k != "database"}
        conn = mysql.connector.connect(**temp_cfg)
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cur.execute(f"USE {DB_CONFIG['database']}")
        conn.commit()
        cur.close()
        conn.close()
    except Error as e:
        raise ConnectionError(f"Cannot create database: {e}")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            username    VARCHAR(80)  UNIQUE NOT NULL,
            email       VARCHAR(150) UNIQUE NOT NULL,
            password    VARCHAR(256) NOT NULL,
            role        ENUM('user','admin') DEFAULT 'user',
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id              INT AUTO_INCREMENT PRIMARY KEY,
            user_id         INT NOT NULL,
            title           VARCHAR(300),
            text_snippet    TEXT,
            full_text       LONGTEXT,
            prediction      ENUM('FAKE','REAL') NOT NULL,
            confidence      FLOAT NOT NULL,
            is_public       TINYINT(1) DEFAULT 0,
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            analysis_id INT NOT NULL,
            user_id     INT NOT NULL,
            vote        ENUM('up','down') NOT NULL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_vote (analysis_id, user_id),
            FOREIGN KEY (analysis_id) REFERENCES analyses(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id)     REFERENCES users(id)    ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            analysis_id INT NOT NULL,
            user_id     INT NOT NULL,
            content     TEXT NOT NULL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (analysis_id) REFERENCES analyses(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id)     REFERENCES users(id)    ON DELETE CASCADE
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
