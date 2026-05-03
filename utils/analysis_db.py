from utils.db import get_connection


def save_analysis(user_id, title, text_snippet, full_text, prediction, confidence, is_public=False):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO analyses
           (user_id, title, text_snippet, full_text, prediction, confidence, is_public)
           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (user_id, title, text_snippet, full_text, prediction, round(confidence, 4), int(is_public)),
    )
    conn.commit()
    analysis_id = cur.lastrowid
    cur.close()
    conn.close()
    return analysis_id


def get_user_history(user_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM analyses WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_public_analyses(limit=50):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """SELECT a.*,
                  u.username,
                  SUM(CASE WHEN v.vote='up'   THEN 1 ELSE 0 END) AS upvotes,
                  SUM(CASE WHEN v.vote='down' THEN 1 ELSE 0 END) AS downvotes
           FROM analyses a
           JOIN users u ON a.user_id = u.id
           LEFT JOIN votes v ON v.analysis_id = a.id
           WHERE a.is_public = 1
           GROUP BY a.id, u.username, a.title, a.text_snippet, a.full_text,
                    a.prediction, a.confidence, a.is_public, a.created_at
           ORDER BY a.created_at DESC
           LIMIT %s""",
        (limit,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_analysis_by_id(analysis_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM analyses WHERE id = %s", (analysis_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def publish_analysis(analysis_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE analyses SET is_public = 1 WHERE id = %s", (analysis_id,))
    conn.commit()
    cur.close()
    conn.close()


def delete_analysis(analysis_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM analyses WHERE id = %s", (analysis_id,))
    conn.commit()
    cur.close()
    conn.close()


def cast_vote(analysis_id, user_id, vote):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO votes (analysis_id, user_id, vote) VALUES (%s, %s, %s)
           ON DUPLICATE KEY UPDATE vote = %s""",
        (analysis_id, user_id, vote, vote),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_vote(analysis_id, user_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT vote FROM votes WHERE analysis_id=%s AND user_id=%s",
        (analysis_id, user_id),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row["vote"] if row else None


def add_comment(analysis_id, user_id, content):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO comments (analysis_id, user_id, content) VALUES (%s, %s, %s)",
        (analysis_id, user_id, content),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_comments(analysis_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """SELECT c.*, u.username FROM comments c
           JOIN users u ON c.user_id = u.id
           WHERE c.analysis_id = %s ORDER BY c.created_at ASC""",
        (analysis_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_stats():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) AS total FROM analyses")
    total = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) AS fake FROM analyses WHERE prediction='FAKE'")
    fake = cur.fetchone()["fake"]
    cur.execute("SELECT COUNT(*) AS users FROM users")
    users = cur.fetchone()["users"]
    cur.execute("SELECT COUNT(*) AS pub FROM analyses WHERE is_public=1")
    pub = cur.fetchone()["pub"]
    cur.close()
    conn.close()
    return {"total": total, "fake": fake, "real": total - fake, "users": users, "public": pub}


def get_all_analyses_admin():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """SELECT a.*, u.username FROM analyses a
           JOIN users u ON a.user_id = u.id
           ORDER BY a.created_at DESC LIMIT 200"""
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
