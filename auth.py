from db import get_conn

def login(username, password):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def register(username, password):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)",
                    (username, password, "user"))
        conn.commit()
        return True
    except:
        return False
